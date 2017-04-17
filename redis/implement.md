#《redis设计与实现》快闪 

##基本数据类型

### 简单动态字符串 sds 

```c
struct sdshdr {
    
    // buf 中已占用空间的长度
    int len;

    // buf 中剩余可用空间的长度
    int free;

    // 数据空间
    char buf[];
};
```

对比c字符串数组的优势
1. 常数复杂度获取字符串长度 (添加记录字符串长度字段)
2. 杜绝缓冲区溢出 (装饰器模式检查是否分配足够内存)
3. 减少修改字符串时带来的内存重分配次数
    1. 预分配
        - 修改字符串之后len < 1MB, 分配额外的free == len
        - 修改字符串之后len >= 1MB, 分配额外的free == 1MB
    2. 惰性空间释放(buf数组中删除元素后仅改变free，不立即进行内存回收)
4. 二进制安全(处理了空字符)


### 链表 list

list实现为双链表


```c
/* Node, List, and Iterator are the only data structures used currently. */

/*
 * 双端链表节点
 */
typedef struct listNode {

    // 前置节点
    struct listNode *prev;

    // 后置节点
    struct listNode *next;

    // 节点的值
    void *value;

} listNode;


/*
 * 双端链表结构
 */
typedef struct list {

    // 表头节点
    listNode *head;

    // 表尾节点
    listNode *tail;

    // 节点值复制函数
    void *(*dup)(void *ptr);

    // 节点值释放函数
    void (*free)(void *ptr);

    // 节点值对比函数
    int (*match)(void *ptr, void *key);

    // 链表所包含的节点数量
    unsigned long len;

} list;
```

无环双链表
1. head->prev == NULL
2. tail->next == NULL

### 字典 dict

使用哈希表实现(hash map)， 使用用拉链法(chaining)解决冲突


```c
/*
 * 哈希表节点
 */
typedef struct dictEntry {
    
    // 键
    void *key;

    // 值
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
    } v;

    // 指向下个哈希表节点，形成链表
    struct dictEntry *next;

} dictEntry;


/*
 * 字典类型特定函数
 */
typedef struct dictType {

    // 计算哈希值的函数
    unsigned int (*hashFunction)(const void *key);

    // 复制键的函数
    void *(*keyDup)(void *privdata, const void *key);

    // 复制值的函数
    void *(*valDup)(void *privdata, const void *obj);

    // 对比键的函数
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);

    // 销毁键的函数
    void (*keyDestructor)(void *privdata, void *key);
    
    // 销毁值的函数
    void (*valDestructor)(void *privdata, void *obj);

} dictType;


/* This is our hash table structure. Every dictionary has two of this as we
 * implement incremental rehashing, for the old to the new table. */
/*
 * 哈希表
 *
 * 每个字典都使用两个哈希表，从而实现渐进式 rehash 。
 */
typedef struct dictht {
    
    // 哈希表数组
    dictEntry **table;

    // 哈希表大小
    unsigned long size;
    
    // 哈希表大小掩码，用于计算索引值
    // 总是等于 size - 1
    unsigned long sizemask;

    // 该哈希表已有节点的数量
    unsigned long used;

} dictht;

/*
 * 字典
 */
typedef struct dict {

    // 类型特定函数
    dictType *type;

    // 私有数据
    void *privdata;

    // 哈希表
    dictht ht[2];

    // rehash 索引
    // 当 rehash 不在进行时，值为 -1
    int rehashidx; /* rehashing not in progress if rehashidx == -1 */

    // 目前正在运行的安全迭代器的数量
    int iterators; /* number of iterators currently running */

} dict;
```


dict每次都有初始化两个dictht主要是为dict内存shrink或者grow之后的rehash做准备。

渐进时rehash策略避免大dict rehash式瞬间造成的巨大时空开销导致服务无响应。


### 跳跃表 skiplist

zset的实现

level为1~32


```c
/* ZSETs use a specialized version of Skiplists */
/*
 * 跳跃表节点
 */
typedef struct zskiplistNode {

    // 成员对象
    robj *obj;

    // 分值
    double score;

    // 后退指针
    struct zskiplistNode *backward;

    // 层
    struct zskiplistLevel {

        // 前进指针
        struct zskiplistNode *forward;

        // 跨度
        unsigned int span;

    } level[];

} zskiplistNode;

/*
 * 跳跃表
 */
typedef struct zskiplist {

    // 表头节点和表尾节点
    struct zskiplistNode *header, *tail;

    // 表中节点的数量
    unsigned long length;

    // 表中层数最大的节点的层数
    int level;

} zskiplist;

/*
 * 有序集合
 */
typedef struct zset {

    // 字典，键为成员，值为分值
    // 用于支持 O(1) 复杂度的按成员取分值操作
    dict *dict;

    // 跳跃表，按分值排序成员
    // 用于支持平均复杂度为 O(log N) 的按分值定位成员操作
    // 以及范围操作
    zskiplist *zsl;

} zset;
```

### 整数集合 intset

```c
typedef struct intset {
    
    // 编码方式
    uint32_t encoding;

    // 集合包含的元素数量
    uint32_t length;

    // 保存元素的数组
    int8_t contents[];

} intset;
```

### 压缩列表 ziplist

ziplist是一种顺序性数据结构，占用内存连续，特点是紧凑


```c
/*
 *  <zlbytes><zltail><zllen><entry><entry><zlend>
 *  <zlbytes> 是一个无符号整数，保存着 ziplist 使用的内存数量。
 *  <zltail> 保存着到达列表中最后一个节点的偏移量。
 *  <zllen> 保存着列表中的节点数量。
 *  <zlend> 的长度为 1 字节，值为 255 ，标识列表的末尾。
 */
 
非空 ziplist 示例图

area        |<---- ziplist header ---->|<----------- entries ------------->|<-end->|

size          4 bytes  4 bytes  2 bytes    ?        ?        ?        ?     1 byte
            +---------+--------+-------+--------+--------+--------+--------+-------+
component   | zlbytes | zltail | zllen | entry1 | entry2 |  ...   | entryN | zlend |
            +---------+--------+-------+--------+--------+--------+--------+-------+
                                       ^                          ^        ^
address                                |                          |        |
                                ZIPLIST_ENTRY_HEAD                |   ZIPLIST_ENTRY_END
                                                                  |
                                                        ZIPLIST_ENTRY_TAIL
```

每个entry中记录了上一个entry的长度和大小，这样可以从当前entry计算出上一个entry的起始地址即指针。


### redis对象

```c
typedef struct redisObject {

    // 类型
    unsigned type:4;

    // 编码
    unsigned encoding:4;

    // 对象最后一次被访问的时间
    unsigned lru:REDIS_LRU_BITS; /* lru time (relative to server.lruclock) */

    // 引用计数
    int refcount;

    // 指向实际值的指针
    void *ptr;

} robj;
```

列表对象实现可以是linkedlist或者ziplist<br>
当列表元素数量小于512并且元素小于64字节时，使用ziplist，否则使用linkedlist

哈希对象实现可以是hashtable或者ziplist<br>
使用ziplist时，key和value分别作为一个entry添加至ziplist, key在前value在后。<br>
当哈希元素键值对数量小于512并且键值entry均小于64字节时，使用ziplist, 否则使用hashtable

集合对象实现可以是intset或者hashtable<br>
当集合元素数量小于512并且所有元素都是整数时使用intset, 否则使用hashtable

有序集合对象实现可以是ziplist或skiplist+hashtable<br>
使用ziplist时，member和score分别作为entry存入ziplist, 并且按照score升序进行排列<br>
当元素数量小于128并且所有元素大小小于64字节时使用ziplist否则使用skiplist+hashtable.

0~9999字符串对象共享机制，类似于CPython的小整数对象.
其他字符串对象不共享。

## 单机数据库的实现

### 数据库

默认创建16个db, 可通过select命令进行切换。

db中有一个dict对象，存放用户存入的key-value。

有一个expire对象保存key的过期时间。

过期key 惰性删除+定期删除。

**持久化机制**
1. RDB 将数据库的快照（snapshot）以二进制的方式保存到磁盘中。
2. AOF 则以协议文本的方式，将所有对数据库进行过写入的命令（及其参数）记录到 AOF 文件，以此达到记录数据库状态的目的。

保存RDB文件不会包含过期key，主服务器模式运行载入RDB不会加载过期key，从服务器模式会加载所有key。

从服务器对于过期键不作处理, 而是像不过期键一样正常返回，只有收到主服务器发来的DEL命令才会删除过期键。

### RDB持久化

SAVE命令是阻塞的。

检测RDB文件自动载入，优先使用AOF文件。

自动保存RDB触发条件为N秒内执行了M次修改。


### AOF(Append Only File)持久化

服务器执行完命令之后, 追加命令至文件。


### 事件

包括文件事件(处理请求)与时间时间(如定期删除过期key)，文件时间基于Reacotr模式，并且封装了IO多路服务的不同实现形式，这与tornado非常相似。

### 客户端

服务器端使用clients链表保存多个客户端状态, 新的client会被添加到链表末尾。

### 服务器

**一个redis命令执行过程**

1. 客户端命令`set key value` 转换为redis协议格式，然后发送给服务器。
2. 服务器端从socket连接中将客户端请求解析后存放在redisClient状态的argc及argv中。<br>
   argc==3, argv[0]==set; argv[1]==key; argv[2]==value
3. 服务器端将调用命令执行器，命令执行器根据argv[0]从command table中查找命令, redisClient->cmd = <redisCommand>。
4. 命令执行器将进行执行命令的准备操作, 包括但不限于:
    1. 检查redisClient->cmd == NULL, 为True则返回错误
    2. 检查redisClient->cmd->arity 确定输入参数个数是否正确
    3. 检查客户端是否通过了身份验证, 未通过身份验证只能执行AUTH命令
    4. 如果服务器设置了maxmemory, 检查内存使用, 如有需要进行内存回收, 回收失败返回错误
    5. 如果上一次执行BGSAVE失败, 并且stop-writes-on-bgsave-error=true, 如果是写命令则返回错误。
    6. 如果客户端正在进行数据载入, 客户端命令必须带有1标示才会被服务器执行
5. 执行命令
6. 命令执行器的后续工作，包括但不限于：
    1. 添加慢查询日志, 如果需要
    2. 更新redisCommand->milliseconds, 同时redisCommand->calls += 1
    3. AOF持久化模块请求将命令写入AOF缓冲区
    4. 如果有正在复制当前服务器，那么将命令传播给所有从服务器
7. 返回客户端执行结果

**serverCron**

serverCron每100ms执行一次

1. redisServer->unixtime与redisServer->mstime 缓存了秒级和毫秒级的unix时间戳, serverCron将更新时间缓存。
2. idletime = redisServer->lrulock - redisObject->lru, serverCron将更新lurlock时间
3. 执行trackOperationPerSecond()用于计算instantaneous_ops_per_sec即一秒钟处理了多少命令请求
4. 更新服务器内存峰值记录stat_peak_memory
5. 处理SIGTERM信号
6. 管理客户端资源，释放链接超时的客户端; 如果客户端缓冲区过大，重新创建默认大小缓冲区
7. 删除过期键；如有必要，shrink字典
8. 执行被延迟的BGREWRITEAOF
9. 检查持久化操作运行状态
10. 将AOF缓冲区的内容写入AOF文件
11. cronloops记录了serverCron执行次数


## 多机数据库的实现

### 复制

**v2.8之前的复制**
1. 从服务器发送sync命令
2. 主服务器执行BGSAVE，并且使用一个缓冲区记录从现在开始执行的所有写命令。
3. 主服务器BGSAVE执行完毕，将生成的RDB文件发送从服务器，从服务器加载RDB文件
4. 主服务器把缓冲区所有写命令发送给从服务器，从服务器执行写命令，同步至主服务器状态。

**部分重同步的实现**
1. 主从服务器都将根据命令长度修改自己的偏移量， 偏移量不同则主从不一致。
2. 主服务器在执行写命令和发送写命令时，都会写一份至复制积压缓冲区，当偏移量差值在缓冲区大小之内时就可以取出缺失的命令发给从服务器。
3. 主从服务器均有id标识，主从服务器会相互保存id，当主从服务器发现id发生变化时，会进行完整重同步操作。


```bash
slaveof <master_ip> <master_port>
```

1. redisServer->masterhost, redisServer->masterport, 返回客户端OK(slaveof为异步命令)
2. 建立主从服务器socket链接
3. 从服务器发送PING命令检查套接字读写状态是否正常
4. 身份验证
5. 从服务器执行 `REPLCONF listening-port <port>` <br> 
   主服务器收到命令redisClient->slave_listening_port = port
6. 同步(完整重同步或部分重同步)
7. 命令传播

**心跳检测**

```c
REPLCONF ACK <replication_offset>
```

1. 检测主从服务器的网络链接状态
2. 辅助实现min-slaves配置选项
3. 检测命令丢失(根据偏移量)

### Sentinel

主服务器下线时，主动将从服务器升级为新的主服务器。

```c
redis-server sentinel.conf --sentinel

redis-sentinel sentinel.conf 
```

### 集群

```c
cluster meet <ip> <port>
```

## 独立功能的实现

### 发布与订阅

```c
subscribe "news.it"

publish "news.it" "hello"

unsubscribe "news.it"

psubscribe "news.*"

punsubscribe "news.*"

pubsub channels
```
当client执行了subscribe "news.it"之后，有客户端执行publish "news.it" "hello"， 所有客户端都会收到该消息。

### 事务

multi -> <multi commands> ->exec

事务队列存放入队命令。

事务的ACID性质。ACID(Atomicity原子性、Consistency一致性、隔离性Isolation、耐久性Durability)

redis事务无回滚功能。

### Lua脚本

```c
EVAL "return 1 + 1" 0
```

### 排序

`sort`

<br><br>

> 参考 <br>
> [1]. [《Redis 设计与实现》](http://redisbook.com/)
