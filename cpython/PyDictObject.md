# CPython字典实现(代码分析)


_**以下针对Python2**_

CPython使用hash table实现python dict，使用开放定址法(open addressing)解决碰撞问题。


```c
typedef struct {
	/* Cached hash code of me_key.  Note that hash codes are C longs.
	 * We have to use Py_ssize_t instead because dict_popitem() abuses
	 * me_hash to hold a search finger.
	 */
	Py_ssize_t me_hash;
	PyObject *me_key;
	PyObject *me_value;
} PyDictEntry;

typedef PyDictEntry dictentry;
```

PyDictEntry / dictentry 是ob_items中存放的一个key-value的结构体。

下文我们用entry指代这一键值对。

 - me_hash: me_key的hash值。
 - me_key: key的PyObject指针。
 - me_value: value的PyObject指针。

```c
/*
There are three kinds of slots in the table:

1. Unused.  me_key == me_value == NULL
   Does not hold an active (key, value) pair now and never did.  Unused can
   transition to Active upon key insertion.  This is the only case in which
   me_key is NULL, and is each slot's initial state.

2. Active.  me_key != NULL and me_key != dummy and me_value != NULL
   Holds an active (key, value) pair.  Active can transition to Dummy upon
   key deletion.  This is the only case in which me_value != NULL.

3. Dummy.  me_key == dummy and me_value == NULL
   Previously held an active (key, value) pair, but that was deleted and an
   active pair has not yet overwritten the slot.  Dummy can transition to
   Active upon key insertion.  Dummy slots cannot be made Unused again
   (cannot have me_key set to NULL), else the probe sequence in case of
   collision would have no way to know they were once active.

Note: .popitem() abuses the me_hash field of an Unused or Dummy slot to
hold a search finger.  The me_hash field of Unused or Dummy slots has no
meaning otherwise.
*/
```

PyDictEntry的三种状态。

1. Unused状态。特点是me_key == me_value == NULL
2. Active状态。特点是me_key != NULL && me_value != NULL
3. Dummy状态。特点是me_key == dummy & me_value == NULL


```c
/* PyDict_MINSIZE is the minimum size of a dictionary.  This many slots are
 * allocated directly in the dict object (in the ma_smalltable member).
 * It must be a power of 2, and at least 4.  8 allows dicts with no more
 * than 5 active entries to live in ma_smalltable (and so avoid an
 * additional malloc); instrumentation suggested this suffices for the
 * majority of dicts (consisting mostly of usually-small instance dicts and
 * usually-small dicts created to pass keyword arguments).
 */
#define PyDict_MINSIZE 8

/*
To ensure the lookup algorithm terminates, there must be at least one Unused
slot (NULL key) in the table.
The value ma_fill is the number of non-NULL keys (sum of Active and Dummy);
ma_used is the number of non-NULL, non-dummy keys (== the number of non-NULL
values == the number of Active items).
To avoid slowing down lookups on a near-full table, we resize the table when
it's two-thirds full.
*/
typedef struct _dictobject PyDictObject;
struct _dictobject {
	PyObject_HEAD
	Py_ssize_t ma_fill;  /* # Active + # Dummy */
	Py_ssize_t ma_used;  /* # Active */

	/* The table contains ma_mask + 1 slots, and that's a power of 2.
	 * We store the mask instead of the size because the mask is more
	 * frequently needed.
	 */
	Py_ssize_t ma_mask;

	/* ma_table points to ma_smalltable for small tables, else to
	 * additional malloc'ed memory.  ma_table is never NULL!  This rule
	 * saves repeated runtime null-tests in the workhorse getitem and
	 * setitem calls.
	 */
	PyDictEntry *ma_table;
	PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
	PyDictEntry ma_smalltable[PyDict_MINSIZE];
};
```

ma_fill: 处于Active + Dummy状态的PyDictEntry数量。<br>
ma_used: 处于Active状态的PyDictEntry数量。<br>
ma_mask: 掩码。等于所拥有的entry数量 - 1，主要作用是通过与运算来得到entry slot的位置索引。<br>
ma_table: 数组指针，指向实际存放entry的数组。<br>
ma_smalltable: 初始化一个大小为8的存放entry的数组。ma_table一开始指向ma_smalltable.<br>
ma_lookup: 函数指针，指向key的查找函数lookdict()或者lookdict_string()<br>

当entry数量超过8个时，ma_table指向额外申请的内存空间，否者指向ma_smalltable。

```c
typedef PyDictObject dictobject;


/* Initialization macros.
   There are two ways to create a dict:  PyDict_New() is the main C API
   function, and the tp_new slot maps to dict_new().  In the latter case we
   can save a little time over what PyDict_New does because it's guaranteed
   that the PyDictObject struct is already zeroed out.
   Everyone except dict_new() should use EMPTY_TO_MINSIZE (unless they have
   an excellent reason not to).
*/

#define INIT_NONZERO_DICT_SLOTS(mp) do {				\
	(mp)->ma_table = (mp)->ma_smalltable;				\
	(mp)->ma_mask = PyDict_MINSIZE - 1;				\
    } while(0)

#define EMPTY_TO_MINSIZE(mp) do {					\
	memset((mp)->ma_smalltable, 0, sizeof((mp)->ma_smalltable));	\
	(mp)->ma_used = (mp)->ma_fill = 0;				\
	INIT_NONZERO_DICT_SLOTS(mp);					\
    } while(0)


PyObject *
PyDict_New(void)
{
	register dictobject *mp;
	if (dummy == NULL) { /* Auto-initialize dummy */
		dummy = PyString_FromString("<dummy key>");
		if (dummy == NULL)
			return NULL;
#ifdef SHOW_CONVERSION_COUNTS
		Py_AtExit(show_counts);
#endif
	}
	if (num_free_dicts) {
		mp = free_dicts[--num_free_dicts];
		assert (mp != NULL);
		assert (mp->ob_type == &PyDict_Type);
		_Py_NewReference((PyObject *)mp);
		if (mp->ma_fill) {
			EMPTY_TO_MINSIZE(mp);
		} else {
			/* At least set ma_table and ma_mask; these are wrong
			   if an empty but presized dict is added to freelist */
			INIT_NONZERO_DICT_SLOTS(mp);
		}
		assert (mp->ma_used == 0);
		assert (mp->ma_table == mp->ma_smalltable);
		assert (mp->ma_mask == PyDict_MINSIZE - 1);
	} else {
		mp = PyObject_GC_New(dictobject, &PyDict_Type);
		if (mp == NULL)
			return NULL;
		EMPTY_TO_MINSIZE(mp);
	}
	mp->ma_lookup = lookdict_string;
#ifdef SHOW_CONVERSION_COUNTS
	++created;
#endif
	_PyObject_GC_TRACK(mp);
	return (PyObject *)mp;
}
```

PyDictObject的初始化过程。

这里可以看出dummy其实是一个PyStringObject，值为`<dummy key>`

这里先将free_dicts缓冲池部分忽略。

1. 创建一个dictobject先申请内存 PyObject_GC_New(dictobject, &PyDict_Type);
2. 然后在EMPTY_TO_MINSIZE宏中进行了一系列赋值操作:
   -  将 ma_smalltable进行清0操作
   - ma_used/ma_filled 置0
   - ma_table指向ma_smalltable
   - ma_make = 7
   - ma_lookup指向lookdict_string
3. 返回dictobject指针。

```c
/*
The basic lookup function used by all operations.
This is based on Algorithm D from Knuth Vol. 3, Sec. 6.4.
Open addressing is preferred over chaining since the link overhead for
chaining would be substantial (100% with typical malloc overhead).

The initial probe index is computed as hash mod the table size. Subsequent
probe indices are computed as explained earlier.

All arithmetic on hash should ignore overflow.

(The details in this version are due to Tim Peters, building on many past
contributions by Reimer Behrends, Jyrki Alakuijala, Vladimir Marangozov and
Christian Tismer).

lookdict() is general-purpose, and may return NULL if (and only if) a
comparison raises an exception (this was new in Python 2.5).
lookdict_string() below is specialized to string keys, comparison of which can
never raise an exception; that function can never return NULL.  For both, when
the key isn't found a dictentry* is returned for which the me_value field is
NULL; this is the slot in the dict at which the key would have been found, and
the caller can (if it wishes) add the <key, value> pair to the returned
dictentry*.
*/
static dictentry *
lookdict(dictobject *mp, PyObject *key, register long hash)
{
	register size_t i;
	register size_t perturb;
	register dictentry *freeslot;
	register size_t mask = (size_t)mp->ma_mask;
	dictentry *ep0 = mp->ma_table;
	register dictentry *ep;
	register int cmp;
	PyObject *startkey;

	i = (size_t)hash & mask;
	ep = &ep0[i];
	if (ep->me_key == NULL || ep->me_key == key)
		return ep;

	if (ep->me_key == dummy)
		freeslot = ep;
	else {
		if (ep->me_hash == hash) {
			startkey = ep->me_key;
			Py_INCREF(startkey);
			cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
			Py_DECREF(startkey);
			if (cmp < 0)
				return NULL;
			if (ep0 == mp->ma_table && ep->me_key == startkey) {
				if (cmp > 0)
					return ep;
			}
			else {
				/* The compare did major nasty stuff to the
				 * dict:  start over.
				 * XXX A clever adversary could prevent this
				 * XXX from terminating.
 				 */
 				return lookdict(mp, key, hash);
 			}
		}
		freeslot = NULL;
	}

	/* In the loop, me_key == dummy is by far (factor of 100s) the
	   least likely outcome, so test for that last. */
	for (perturb = hash; ; perturb >>= PERTURB_SHIFT) {
		i = (i << 2) + i + perturb + 1;
		ep = &ep0[i & mask];
		if (ep->me_key == NULL)
			return freeslot == NULL ? ep : freeslot;
		if (ep->me_key == key)
			return ep;
		if (ep->me_hash == hash && ep->me_key != dummy) {
			startkey = ep->me_key;
			Py_INCREF(startkey);
			cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
			Py_DECREF(startkey);
			if (cmp < 0)
				return NULL;
			if (ep0 == mp->ma_table && ep->me_key == startkey) {
				if (cmp > 0)
					return ep;
			}
			else {
				/* The compare did major nasty stuff to the
				 * dict:  start over.
				 * XXX A clever adversary could prevent this
				 * XXX from terminating.
 				 */
 				return lookdict(mp, key, hash);
 			}
		}
		else if (ep->me_key == dummy && freeslot == NULL)
			freeslot = ep;
	}
	assert(0);	/* NOT REACHED */
	return 0;
}
```

先看一下lookdict的函数定义

```c
static *dictentry lookdict(dictobject *mp, PyObject *key, register long hash)
```

接收三个参数：
1. mp: dictobject指针
2. key: PyObject指针
3. hash: C long类型

lookdict函数在不发生异常的情况下一定会返回一个entry，否则返回NULL.

1. 根据hash与mask进行与运算获得slot索引i
2. 从mp->ma_table中取出对应的entry的指针ep
3. 如果ep->me_key==NULL, 说明改entry处于Unused状态直接返回ep 
4. 如果ep->me_key == key， 说明entry处于Active状态并且就是要找的key，同样直接返回ep
5. 如果ep->me_key == dummy, 这个时候设置了标志位freeslot = ep
6. 接下来一种情况就是ep->me_key处于active状态但key的指针不同, 这时判断ep->me_hash是否等于hash,
   如果ep->me_hash == hash, 将ep->me_key与key的值进行比较，如果相同返回ep，如果不同那么继续
7. 现在ep->me_key不是要找的key，因此要使用探测函数找到下一个位置:
    `i = (i << 2) + i + perturb + 1;` <br>
     这里如果ep->me_key==NULL并且freeslot!=NULL，那么会返回freeslot
     也就是说dummy状态的entry是可以被**重用**的。

在插入和查找key时，寻找插入位置使用的都是lookdict()函数。


```c
/*
 * Hacked up version of lookdict which can assume keys are always strings;
 * this assumption allows testing for errors during PyObject_RichCompareBool()
 * to be dropped; string-string comparisons never raise exceptions.  This also
 * means we don't need to go through PyObject_RichCompareBool(); we can always
 * use _PyString_Eq() directly.
 *
 * This is valuable because dicts with only string keys are very common.
 */
static dictentry *
lookdict_string(dictobject *mp, PyObject *key, register long hash)
{
	register size_t i;
	register size_t perturb;
	register dictentry *freeslot;
	register size_t mask = (size_t)mp->ma_mask;
	dictentry *ep0 = mp->ma_table;
	register dictentry *ep;

	/* Make sure this function doesn't have to handle non-string keys,
	   including subclasses of str; e.g., one reason to subclass
	   strings is to override __eq__, and for speed we don't cater to
	   that here. */
	if (!PyString_CheckExact(key)) {
#ifdef SHOW_CONVERSION_COUNTS
		++converted;
#endif
		mp->ma_lookup = lookdict;
		return lookdict(mp, key, hash);
	}
	i = hash & mask;
	ep = &ep0[i];
	if (ep->me_key == NULL || ep->me_key == key)
		return ep;
	if (ep->me_key == dummy)
		freeslot = ep;
	else {
		if (ep->me_hash == hash && _PyString_Eq(ep->me_key, key))
			return ep;
		freeslot = NULL;
	}

	/* In the loop, me_key == dummy is by far (factor of 100s) the
	   least likely outcome, so test for that last. */
	for (perturb = hash; ; perturb >>= PERTURB_SHIFT) {
		i = (i << 2) + i + perturb + 1;
		ep = &ep0[i & mask];
		if (ep->me_key == NULL)
			return freeslot == NULL ? ep : freeslot;
		if (ep->me_key == key
		    || (ep->me_hash == hash
		        && ep->me_key != dummy
			&& _PyString_Eq(ep->me_key, key)))
			return ep;
		if (ep->me_key == dummy && freeslot == NULL)
			freeslot = ep;
	}
	assert(0);	/* NOT REACHED */
	return 0;
}
```

lookdict_string()是lookdict()的一种特例。因为所有key都为字符串的dict非常常见所以单独写了一个函数。

执行过程中会通过PyString_CheckExact(key)对所有key进行检查，检查不通过那么mp->ma_lookup=lookdict

和lookdict()的区别在于key比较直接进行字符串比较，并且不会发生异常。


```c
/*
Internal routine to insert a new item into the table.
Used both by the internal resize routine and by the public insert routine.
Eats a reference to key and one to value.
Returns -1 if an error occurred, or 0 on success.
*/
static int
insertdict(register dictobject *mp, PyObject *key, long hash, PyObject *value)
{
	PyObject *old_value;
	register dictentry *ep;
	typedef PyDictEntry *(*lookupfunc)(PyDictObject *, PyObject *, long);

	assert(mp->ma_lookup != NULL);
	ep = mp->ma_lookup(mp, key, hash);
	if (ep == NULL) {
		Py_DECREF(key);
		Py_DECREF(value);
		return -1;
	}
	if (ep->me_value != NULL) {
		old_value = ep->me_value;
		ep->me_value = value;
		Py_DECREF(old_value); /* which **CAN** re-enter */
		Py_DECREF(key);
	}
	else {
		if (ep->me_key == NULL)
			mp->ma_fill++;
		else {
			assert(ep->me_key == dummy);
			Py_DECREF(dummy);
		}
		ep->me_key = key;
		ep->me_hash = (Py_ssize_t)hash;
		ep->me_value = value;
		mp->ma_used++;
	}
	return 0;
}
```

插入过程
1. 通过mp->lookup获取可插入的entry
2. 如果ep->me_value!=NULL, 替换value，并调整相关的引用计数，同时ma_used/ma_fill等都无需变化。<br>
   如果ep->me_key == NULL, 那么也就是新加入的entry，那么要将ma_fill + 1<br>
   如果ep->me_key == dummy, 那么要将dummy引用计数 - 1，而且不需要调整ma_fill
   
   
```c
/* CAUTION: PyDict_SetItem() must guarantee that it won't resize the
 * dictionary if it's merely replacing the value for an existing key.
 * This means that it's safe to loop over a dictionary with PyDict_Next()
 * and occasionally replace a value -- but you can't insert new keys or
 * remove them.
 */
int
PyDict_SetItem(register PyObject *op, PyObject *key, PyObject *value)
{
	register dictobject *mp;
	register long hash;
	register Py_ssize_t n_used;

	if (!PyDict_Check(op)) {
		PyErr_BadInternalCall();
		return -1;
	}
	assert(key);
	assert(value);
	mp = (dictobject *)op;
	if (PyString_CheckExact(key)) {
		hash = ((PyStringObject *)key)->ob_shash;
		if (hash == -1)
			hash = PyObject_Hash(key);
	}
	else {
		hash = PyObject_Hash(key);
		if (hash == -1)
			return -1;
	}
	assert(mp->ma_fill <= mp->ma_mask);  /* at least one empty slot */
	n_used = mp->ma_used;
	Py_INCREF(value);
	Py_INCREF(key);
	if (insertdict(mp, key, hash, value) != 0)
		return -1;
	/* If we added a key, we can safely resize.  Otherwise just return!
	 * If fill >= 2/3 size, adjust size.  Normally, this doubles or
	 * quaduples the size, but it's also possible for the dict to shrink
	 * (if ma_fill is much larger than ma_used, meaning a lot of dict
	 * keys have been * deleted).
	 *
	 * Quadrupling the size improves average dictionary sparseness
	 * (reducing collisions) at the cost of some memory and iteration
	 * speed (which loops over every possible entry).  It also halves
	 * the number of expensive resize operations in a growing dictionary.
	 *
	 * Very large dictionaries (over 50K items) use doubling instead.
	 * This may help applications with severe memory constraints.
	 */
	if (!(mp->ma_used > n_used && mp->ma_fill*3 >= (mp->ma_mask+1)*2))
		return 0;
	return dictresize(mp, (mp->ma_used > 50000 ? 2 : 4) * mp->ma_used);
}
```

插入key-value之后，检查是否需要调整mp->ma_table, 当ma_table的装载率超过2/3时，就需要调整ma_table的大小。

注意这里传给dictresize()的第二个参数：
1. 当ma_used > 50000时，为2 * ma_used
2. 当ma_used <= 50000时，为4 * ma_used

说明50,000是一个ma_table大小分界线。

```c
/*
Restructure the table by allocating a new table and reinserting all
items again.  When entries have been deleted, the new table may
actually be smaller than the old one.
*/
static int
dictresize(dictobject *mp, Py_ssize_t minused)
{
	Py_ssize_t newsize;
	dictentry *oldtable, *newtable, *ep;
	Py_ssize_t i;
	int is_oldtable_malloced;
	dictentry small_copy[PyDict_MINSIZE];

	assert(minused >= 0);

	/* Find the smallest table size > minused. */
	for (newsize = PyDict_MINSIZE;
	     newsize <= minused && newsize > 0;
	     newsize <<= 1)
		;
	if (newsize <= 0) {
		PyErr_NoMemory();
		return -1;
	}

	/* Get space for a new table. */
	oldtable = mp->ma_table;
	assert(oldtable != NULL);
	is_oldtable_malloced = oldtable != mp->ma_smalltable;

	if (newsize == PyDict_MINSIZE) {
		/* A large table is shrinking, or we can't get any smaller. */
		newtable = mp->ma_smalltable;
		if (newtable == oldtable) {
			if (mp->ma_fill == mp->ma_used) {
				/* No dummies, so no point doing anything. */
				return 0;
			}
			/* We're not going to resize it, but rebuild the
			   table anyway to purge old dummy entries.
			   Subtle:  This is *necessary* if fill==size,
			   as lookdict needs at least one virgin slot to
			   terminate failing searches.  If fill < size, it's
			   merely desirable, as dummies slow searches. */
			assert(mp->ma_fill > mp->ma_used);
			memcpy(small_copy, oldtable, sizeof(small_copy));
			oldtable = small_copy;
		}
	}
	else {
		newtable = PyMem_NEW(dictentry, newsize);
		if (newtable == NULL) {
			PyErr_NoMemory();
			return -1;
		}
	}

	/* Make the dict empty, using the new table. */
	assert(newtable != oldtable);
	mp->ma_table = newtable;
	mp->ma_mask = newsize - 1;
	memset(newtable, 0, sizeof(dictentry) * newsize);
	mp->ma_used = 0;
	i = mp->ma_fill;
	mp->ma_fill = 0;

	/* Copy the data over; this is refcount-neutral for active entries;
	   dummy entries aren't copied over, of course */
	for (ep = oldtable; i > 0; ep++) {
		if (ep->me_value != NULL) {	/* active entry */
			--i;
			insertdict_clean(mp, ep->me_key, (long)ep->me_hash,
					 ep->me_value);
		}
		else if (ep->me_key != NULL) {	/* dummy entry */
			--i;
			assert(ep->me_key == dummy);
			Py_DECREF(ep->me_key);
		}
		/* else key == value == NULL:  nothing to do */
	}

	if (is_oldtable_malloced)
		PyMem_DEL(oldtable);
	return 0;
}
```

这里根据minused参数来确定ma_table的newsize, 具体策略为从8开始不停左移一位，直到newsize > minused.

举个例子来说, 一个dict ma_used为6，mask+1为8，这个时候装载率等于2/3, 要进行resize.

于是:

```c
minused = 4 * ma_used = 24
8 << 1 == 16 < 24
16 << 1 == 32 > 24
```

于是newsize = 32

这个时候会对mp进行一系列调整，ma_table指向新申请的newsize大小的内存。ma_mask等也作相应调整。

然后需要把就ma_table中的entry全部按照新的mask复制到新的ma_table中。
1. Active状态的entry会被放到新的位置。
2. Dummy状态的entry会被调整引用计数后丢弃。

接着删除旧的ma_table.

注意resize这里包含了grow和shrink两个过程。

```c
int
PyDict_DelItem(PyObject *op, PyObject *key)
{
	register dictobject *mp;
	register long hash;
	register dictentry *ep;
	PyObject *old_value, *old_key;

	if (!PyDict_Check(op)) {
		PyErr_BadInternalCall();
		return -1;
	}
	assert(key);
	if (!PyString_CheckExact(key) ||
	    (hash = ((PyStringObject *) key)->ob_shash) == -1) {
		hash = PyObject_Hash(key);
		if (hash == -1)
			return -1;
	}
	mp = (dictobject *)op;
	ep = (mp->ma_lookup)(mp, key, hash);
	if (ep == NULL)
		return -1;
	if (ep->me_value == NULL) {
		set_key_error(key);
		return -1;
	}
	old_key = ep->me_key;
	Py_INCREF(dummy);
	ep->me_key = dummy;
	old_value = ep->me_value;
	ep->me_value = NULL;
	mp->ma_used--;
	Py_DECREF(old_value);
	Py_DECREF(old_key);
	return 0;
}
```

删除过程就是找到key对应的entry，将其设置为dummy.


```c
ShowDictObject(dictobject* mp)
{
    dictentry *entry = mp->ma_table;
    int count = mp->ma_mask + 1;
    int i;
    printf("key  :");
    for(i = 0; i < count; ++i) {
        PyObject *key = entry->me_key;
        if(key == NULL) {
            printf("NULL");
        }
        else {
            if(PyString_Check(key)) {
                if(PyString_AsString(key)[0] == '<') {
                    printf("dummy");
                }
                else {
                    (key->ob_type)->tp_print(key, stdout, 0);
                }
            }
            else {
                (key->ob_type)->tp_print(key, stdout, 0);
            }
        }
        printf("\t");
        ++entry;
    }

    printf("\nvalue: ");
    entry = mp->ma_table;
    for (i = 0; i < count;  ++i) {
        PyObject *value = entry->me_value;
        if (value == NULL) {
            printf("NULL");
        }
        else {
            (value->ob_type)->tp_print(value, stdout, 0);
        }
        printf("\t");
        ++entry;
    }
    printf("\n");
}

static int
insertdict(register dictobject *mp, PyObject *key, long hash, PyObject *value)
{
    PyObject *old_value;
    register dictentry *ep;
    typedef PyDictEntry *(*lookupfunc)(PyDictObject *, PyObject *, long);

    assert(mp->ma_lookup != NULL);
    ep = mp->ma_lookup(mp, key, hash);
    if (ep == NULL) {
        Py_DECREF(key);
        Py_DECREF(value);
        return -1;
    }
    if (ep->me_value != NULL) {
        old_value = ep->me_value;
        ep->me_value = value;
        Py_DECREF(old_value); /* which **CAN** re-enter */
        Py_DECREF(key);
    }
    else {
        if (ep->me_key == NULL)
            mp->ma_fill++;
        else {
            assert(ep->me_key == dummy);
            Py_DECREF(dummy);
        }
        ep->me_key = key;
        ep->me_hash = (Py_ssize_t)hash;
        ep->me_value = value;
        mp->ma_used++;
    }
    /*
    添加过滤 key为"HO" 则打印整个dict
    */
    dictentry *p;
    long str_hash;
    PyObject *str = PyString_FromString("HO");
    str_hash = PyObject_Hash(str);
    p = mp->ma_lookup(mp, str, str_hash);
        p = mp->ma_lookup(mp, str, str_hash);
    if (p->me_value != NULL && (key->ob_type)->tp_name[0] == 'i') {
         PyIntObject *int_object = (PyIntObject*)key;
         printf("insert %ld\n", int_object->ob_ival);
         ShowDictObject(mp);
    }
    
    return 0;
}
```

添加打印PyDictObject打印函数，并在在insertdict中添加hook.

```python
>>> d = {'HO':1}
>>> d
{'HO': 1}
>>> d[9]=9
insert 9
key  :NULL	9	NULL	NULL	NULL	'HO'	NULL	NULL
value: NULL	9	NULL	NULL	NULL	1	NULL	NULL
>>> d[17]=17
insert 17
key  :NULL	9	NULL	NULL	NULL	'HO'	NULL	17
value: NULL	9	NULL	NULL	NULL	1	NULL	17
>>> del d[9]
>>> d[17] = 16
insert 17
key  :NULL	dummy	NULL	NULL	NULL	'HO'	NULL	17
value: NULL	NULL	NULL	NULL	NULL	1	NULL	16
>>> del d[17]
>>> d[17]=17
insert 17
key  :NULL	17	NULL	NULL	NULL	'HO'	NULL	dummy
value: NULL	17	NULL	NULL	NULL	1	NULL	NULL
>>>
```

以上是重新编译python后的测试结果。
注意key=9与key=17会碰撞

```python
In [111]: hash(9) & 7
Out[111]: 1

In [112]: hash(17) & 7
Out[112]: 1o
```

更多内容请前往 [leohowell.com](https://leohowell.com)

> 参考 <br>
> [1]. 《Python源码剖析》<br>
> [2]. https://github.com/python/cpython
