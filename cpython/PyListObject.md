# CPython列表实现(代码分析)


```c
typedef struct {
    PyObject_VAR_HEAD
    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
    PyObject **ob_item;

    /* ob_item contains space for 'allocated' elements.  The number
     * currently in use is ob_size.
     * Invariants:
     *     0 <= ob_size <= allocated
     *     len(list) == ob_size
     *     ob_item == NULL implies ob_size == allocated == 0
     * list.sort() temporarily sets allocated to -1 to detect mutations.
     *
     * Items must normally not be NULL, except during construction when
     * the list is not yet visible outside the function that builds it.
     */
    Py_ssize_t allocated;
} PyListObject;
```

可以看到 len(list) == ob_size, 说明ob_size中存放的是列表中元素的实际个数。

allocated则等于当前list已经分配的内存大小。


```c
/* Empty list reuse scheme to save calls to malloc and free */
#define MAXFREELISTS 80
static PyListObject *free_lists[MAXFREELISTS];
static int num_free_lists = 0;

PyObject *
PyList_New(Py_ssize_t size)
{
	PyListObject *op;
	size_t nbytes;

	if (size < 0) {
		PyErr_BadInternalCall();
		return NULL;
	}
	nbytes = size * sizeof(PyObject *);
	/* Check for overflow without an actual overflow,
	 *  which can cause compiler to optimise out */
	if (size > PY_SIZE_MAX / sizeof(PyObject *))
		return PyErr_NoMemory();
	if (num_free_lists) {
		num_free_lists--;
		op = free_lists[num_free_lists];
		_Py_NewReference((PyObject *)op);
	} else {
		op = PyObject_GC_New(PyListObject, &PyList_Type);
		if (op == NULL)
			return NULL;
	}
	if (size <= 0)
		op->ob_item = NULL;
	else {
		op->ob_item = (PyObject **) PyMem_MALLOC(nbytes);
		if (op->ob_item == NULL) {
			Py_DECREF(op);
			return PyErr_NoMemory();
		}
		memset(op->ob_item, 0, nbytes);
	}
	op->ob_size = size;
	op->allocated = size;
	_PyObject_GC_TRACK(op);
	return (PyObject *) op;
}
```

free_lists是大小为80的对象缓冲池。

```c
int
PyList_SetItem(register PyObject *op, register Py_ssize_t i,
               register PyObject *newitem)
{
	register PyObject *olditem;
	register PyObject **p;
	if (!PyList_Check(op)) {
		Py_XDECREF(newitem);
		PyErr_BadInternalCall();
		return -1;
	}
	if (i < 0 || i >= ((PyListObject *)op) -> ob_size) {
		Py_XDECREF(newitem);
		PyErr_SetString(PyExc_IndexError,
				"list assignment index out of range");
		return -1;
	}
	p = ((PyListObject *)op) -> ob_item + i;
	olditem = *p;
	*p = newitem;
	Py_XDECREF(olditem);
	return 0;
}
```

olditem引用计数会减少1。


```c
/* Ensure ob_item has room for at least newsize elements, and set
 * ob_size to newsize.  If newsize > ob_size on entry, the content
 * of the new slots at exit is undefined heap trash; it's the caller's
 * responsiblity to overwrite them with sane values.
 * The number of allocated elements may grow, shrink, or stay the same.
 * Failure is impossible if newsize <= self.allocated on entry, although
 * that partly relies on an assumption that the system realloc() never
 * fails when passed a number of bytes <= the number of bytes last
 * allocated (the C standard doesn't guarantee this, but it's hard to
 * imagine a realloc implementation where it wouldn't be true).
 * Note that self->ob_item may change, and even if newsize is less
 * than ob_size on entry.
 */
static int
list_resize(PyListObject *self, Py_ssize_t newsize)
{
	PyObject **items;
	size_t new_allocated;
	Py_ssize_t allocated = self->allocated;

	/* Bypass realloc() when a previous overallocation is large enough
	   to accommodate the newsize.  If the newsize falls lower than half
	   the allocated size, then proceed with the realloc() to shrink the list.
	*/
	if (allocated >= newsize && newsize >= (allocated >> 1)) {
		assert(self->ob_item != NULL || newsize == 0);
		self->ob_size = newsize;
		return 0;
	}

	/* This over-allocates proportional to the list size, making room
	 * for additional growth.  The over-allocation is mild, but is
	 * enough to give linear-time amortized behavior over a long
	 * sequence of appends() in the presence of a poorly-performing
	 * system realloc().
	 * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
	 */
	new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);

	/* check for integer overflow */
	if (new_allocated > PY_SIZE_MAX - newsize) {
		PyErr_NoMemory();
		return -1;
	} else {
		new_allocated += newsize;
	}

	if (newsize == 0)
		new_allocated = 0;
	items = self->ob_item;
	if (new_allocated <= ((~(size_t)0) / sizeof(PyObject *)))
		PyMem_RESIZE(items, PyObject *, new_allocated);
	else
		items = NULL;
	if (items == NULL) {
		PyErr_NoMemory();
		return -1;
	}
	self->ob_item = items;
	self->ob_size = newsize;
	self->allocated = new_allocated;
	return 0;
}

static int
ins1(PyListObject *self, Py_ssize_t where, PyObject *v)
{
	Py_ssize_t i, n = self->ob_size;
	PyObject **items;
	if (v == NULL) {
		PyErr_BadInternalCall();
		return -1;
	}
	if (n == PY_SSIZE_T_MAX) {
		PyErr_SetString(PyExc_OverflowError,
			"cannot add more objects to list");
		return -1;
	}

	if (list_resize(self, n+1) == -1)
		return -1;

	if (where < 0) {
		where += n;
		if (where < 0)
			where = 0;
	}
	if (where > n)
		where = n;
	items = self->ob_item;
	for (i = n; --i >= where; )
		items[i+1] = items[i];
	Py_INCREF(v);
	items[where] = v;
	return 0;
}

int
PyList_Insert(PyObject *op, Py_ssize_t where, PyObject *newitem)
{
	if (!PyList_Check(op)) {
		PyErr_BadInternalCall();
		return -1;
	}
	return ins1((PyListObject *)op, where, newitem);
}
```

list_resize可以确保ob_items中有足够的空间容纳新元素，同时也能减少空间以节省内存。


```python
>>> a = []
>>> a.insert(99, 0)
>>> a
>>> [0]
>>> a.insert(-100, 1)
>>> a
>>> [1, 0]
```

值得注意的是插入到任何位置都是合法的。

```c
static int
app1(PyListObject *self, PyObject *v)
{
	Py_ssize_t n = PyList_GET_SIZE(self);

	assert (v != NULL);
	if (n == PY_SSIZE_T_MAX) {
		PyErr_SetString(PyExc_OverflowError,
			"cannot add more objects to list");
		return -1;
	}

	if (list_resize(self, n+1) == -1)
		return -1;

	Py_INCREF(v);
	PyList_SET_ITEM(self, n, v);
	return 0;
}

int
PyList_Append(PyObject *op, PyObject *newitem)
{
	if (PyList_Check(op) && (newitem != NULL))
		return app1((PyListObject *)op, newitem);
	PyErr_BadInternalCall();
	return -1;
}
```

append实际调用了PyList_SetItem()。


```c
static void
list_dealloc(PyListObject *op)
{
	Py_ssize_t i;
	PyObject_GC_UnTrack(op);
	Py_TRASHCAN_SAFE_BEGIN(op)
	if (op->ob_item != NULL) {
		/* Do it backwards, for Christian Tismer.
		   There's a simple test case where somehow this reduces
		   thrashing when a *very* large list is created and
		   immediately deleted. */
		i = op->ob_size;
		while (--i >= 0) {
			Py_XDECREF(op->ob_item[i]);
		}
		PyMem_FREE(op->ob_item);
	}
	if (num_free_lists < MAXFREELISTS && PyList_CheckExact(op))
		free_lists[num_free_lists++] = op;
	else
		op->ob_type->tp_free((PyObject *)op);
	Py_TRASHCAN_SAFE_END(op)
}
```

1. 将ob_items中元素引用计数减1，然后释放内存。
2. free_lists不满则将PyListObject放入free_lists，否则进行内存释放。


```c
static int
list_print(PyListObject *op, FILE *fp, int flags)
{
	int rc;
	Py_ssize_t i;

	rc = Py_ReprEnter((PyObject*)op);
	if (rc != 0) {
		if (rc < 0)
			return rc;
		fprintf(fp, "[...]");
		return 0;
	}
	fprintf(fp, "[");
	for (i = 0; i < op->ob_size; i++) {
		if (i > 0)
			fprintf(fp, ", ");
		if (PyObject_Print(op->ob_item[i], fp, 0) != 0) {
			Py_ReprLeave((PyObject *)op);
			return -1;
		}
	}
	fprintf(fp, "]");
	printf("\nallocated=%d, ob_size=%d\n", op->allocated, op->ob_size);
	Py_ReprLeave((PyObject *)op);
	return 0;
}
```

加入了打印allocated与ob_size语句。


```python
>>> a = []
>>> a
[]
allocated=0, ob_size=0

>>> a.append('1')
>>> a
['1']
allocated=4, ob_size=1

>>> a.append('2')
>>> a
['1', '2']
allocated=4, ob_size=2

>>> a.append('3')
>>> a
['1', '2', '3']
allocated=4, ob_size=3

>>> a.append('4')
>>> a
['1', '2', '3', '4']
allocated=4, ob_size=4

>>> a.append('5')
>>> a
['1', '2', '3', '4', '5']
allocated=8, ob_size=5

>>> a.append('6')
>>> a
['1', '2', '3', '4', '5', '6']
allocated=8, ob_size=6
```

这是list内存grow过程。

```python
>>> a = ['1','2','3','4','5']
>>> a.pop()
'5'
>>> a
['1', '2', '3', '4']
allocated=5, ob_size=4

>>> a.pop()
'4'
>>> a
['1', '2', '3']
allocated=5, ob_size=3

>>> a.pop()
'3'
>>> a
['1', '2']
allocated=5, ob_size=2

>>> a.pop()
'2'
>>> a
['1']
allocated=4, ob_size=1

>>> a.pop()
'1'
>>> a
[]
allocated=0, ob_size=0
```

这是list内存shrink过程。


更多实现请前往 [leohowell.com](https://leohowell.com)
