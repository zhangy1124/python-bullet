# Simple bash command example

### 1. file

```bash 
$ file test.txt
test.txt: ASCII text

$ file a.awk
a.awk: awk script, UTF-8 Unicode text executable

$ file redis-stable.tar.gz
redis-stable.tar.gz: gzip compressed data, from Unix, last modified: Sun Feb 12 23:15:45 2017

$ file redis-stable
redis-stable: directory
```

### 2. find

find <location> <comparison-criteria> <comparison-criteria>

run find without any argument will **lists out all the files** in the current directory as well as the subdirectories in the current directory.

```bash
$ find . -name 'tornado*'
./.cache/pip/wheels/b3/db/47/46e05d1ee3ecfba252fcab42f0a156dab0df0cddf99fa0827c/tornado-4.4.2-cp27-cp27mu-linux_x86_64.whl


# Show file detail
$ find . -name 'tornado*' -ls
135764  400 -rw-r--r--   1 root     root       408943 Feb  8 11:52 ./.cache/pip/wheels/b3/db/47/46e05d1ee3ecfba252fcab42f0a156dab0df0cddf99fa0827c/tornado-4.4.2-cp27-cp27mu-linux_x86_64.whl


# Ignore case
$ find . -iname '*.O'
./deps/jemalloc/src/huge.o
./deps/jemalloc/src/mutex.o


# Limit depth of directory traversal
$ find . -maxdepth 2 -iname '*.O'
./src/endianconv.o
./src/redis-cli.o
./src/blocked.o


# Invert match
$ find . -not -name '*.o'
.
./utils
./utils/hashtable


# multiple search filter
$ find . -name '*.conf'
./sentinel.conf
./tests/assets/default.conf
./redis.conf
$ find . -name '*.conf' ! -name "default.*"
./sentinel.conf
./redis.conf
$ find . -name '*.conf' -o -name "*.txt"
./sentinel.conf
./tests/assets/default.conf
./deps/jemalloc/include/jemalloc/internal/public_symbols.txt
./deps/jemalloc/include/jemalloc/internal/private_symbols.txt
./redis.conf


# Search only files or only directories
$ find . -type f -name "*.conf"
./sentinel.conf
./tests/assets/default.conf
./redis.conf
$ find . -type d -name "src"
./deps/jemalloc/test/src
./deps/jemalloc/src
./deps/lua/src
./src


# Search multiple directories together
$ find src/ deps/ -name "*c"


# Find files changed in last N minutes.
$ find . -cmin -60
.
./.viminfo
./test.txt


# Find files in a size range
$ find / -size +100M -size -1024M
/sys/devices/pci0000:00/0000:00:0f.0/resource1_wc
/sys/devices/pci0000:00/0000:00:0f.0/resource1
```

### 3. locate
locate actually search a built-in database, named locate.db.
 
update the database manually(might take a few minutes): `updatedb`

```bash
$ locate "*.tar.gz"
/opt/env/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/opt/homework/reflector/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/opt/twitter/env/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/root/redis-stable.tar.gz


# Ignore case
$ locate -i "TAR.GZ"
/opt/env/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/opt/homework/reflector/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/opt/twitter/env/lib/python2.7/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
/root/redis-stable.tar.gz
```

### 4. gzip & gunzip

```bash
$ gzip test.txt
$ ls
a.awk  redis-stable  redis-stable.tar.gz  test.txt.gz

$ gunzip test.txt.gz
$ ls
a.awk  redis-stable  redis-stable.tar.gz  test.txt
```

### 5. gzcat & zcat
Lets you look at gzipped file without actually having to gunzip it.

```bash
$ zcat test.txt.gz
Active Internet connections (w/o servers) a
Proto Recv-Q Send-Q Local Address           Foreign Address         State
...
```

### 6. touch
Updates access and modification time stamps of your file. If it doesn't exists, it'll be created.

```bash
$ ll test.txt
-rw-r--r-- 1 root root 1520 Mar 10 17:18 test.txt
$ touch test.txt
$ ll test.txt
-rw-r--r-- 1 root root 1520 Apr 27 10:05 test.txt
```

### 7. nl
Number lines of files

```bash
$ cat example.txt
iLorem ipsum
dolor sit amet,
consetetur
sadipscing elitr,
sed diam nonumy

$ nl -s ". " example.txt
     1. iLorem ipsum
     2. dolor sit amet,
     3. consetetur
     4. sadipscing elitr,
     5. sed diam nonumy
```

### 8. sed

```bash
$ cat tmp.txt
Hello This is a Test 1 2 3 4
$ sed "s/ /-/g" tmp.txt
Hello-This-is-a-Test-1-2-3-4
$ sed "s/[0-9]/*/g" tmp.txt
Hello This is a Test * * * *
```

### 9. sort

```bash
$ cat tmp.txt
f
b
c
g
a
e
d
$ sort tmp.txt
a
b
c
d
e
f
g
$ sort tmp.txt | sort -R
b
f
e
d
a
c
g
```

### 10. tr

```bash
$ cat tmp.txt
Hello World Foo Bar Baz!
$ cat tmp.txt | tr 'a-z' 'A-Z'
HELLO WORLD FOO BAR BAZ!
$ cat tmp.txt | tr ' ' '\n'
Hello
World
Foo
Bar
Baz!
```

### 11. uniq

```bash
$ cat tmp.txt
a
a
b
a
b
c
d
c
$ uniq tmp.txt
a
b
a
b
c
d
c
$ uniq tmp.txt -c
      2 a
      1 b
      1 a
      1 b
      1 c
      1 d
      1 c
```

### 12. wc

```bash
$ wc test.txt
  23  159 1520 test.txt
  
Where 23 is lines, 159 is words and 1520 is characters.
```

### 13. dig

Domain Information Groper

```bash
$ dig leohowell.com

; <<>> DiG 9.9.5-3ubuntu0.8-Ubuntu <<>> leohowell.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40652
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; MBZ: 0005 , udp: 4000
;; QUESTION SECTION:
;leohowell.com.			IN	A

;; ANSWER SECTION:
leohowell.com.		5	IN	A	163.44.169.240

;; Query time: 353 msec
;; SERVER: 192.168.2.2#53(192.168.2.2)
;; WHEN: Thu Apr 27 10:20:36 CST 2017
;; MSG SIZE  rcvd: 58

$ dig @8.8.8.8 leohowell.com +noall +answer

; <<>> DiG 9.9.5-3ubuntu0.8-Ubuntu <<>> @8.8.8.8 leohowell.com +noall +answer
; (1 server found)
;; global options: +cmd
leohowell.com.		401	IN	A	163.44.169.240
```

### 14. last

```bash
$ last root
root     pts/0        192.168.2.1      Fri Mar 10 15:59   still logged in
root     pts/0        192.168.2.1      Wed Mar  8 00:12 - 06:52  (06:40)
root     pts/0        192.168.2.1      Wed Mar  8 00:12 - 00:12  (00:00)
root     pts/0        192.168.2.1      Tue Mar  7 20:55 - 00:11  (03:16)
root     pts/0        192.168.2.1      Tue Mar  7 20:47 - 20:55  (00:08)
root     pts/0        192.168.2.1      Tue Mar  7 20:24 - 20:29  (00:04)
root     pts/0        192.168.2.1      Tue Mar  7 20:24 - 20:24  (00:00)
root     pts/0        192.168.2.1      Tue Mar  7 20:24 - 20:24  (00:00)
root     pts/0        192.168.2.1      Tue Mar  7 18:22 - 19:40  (01:18)
root     pts/0        192.168.2.1      Mon Mar  6 16:40 - 15:13  (22:32)
root     pts/0        192.168.2.1      Mon Mar  6 15:37 - 16:40  (01:03)
root     pts/0        192.168.2.1      Sun Mar  5 21:30 - 15:36  (18:05)
root     pts/0        192.168.2.1      Sun Mar  5 16:42 - 18:48  (02:06)
root     pts/0        192.168.2.1      Wed Mar  1 19:42 - 13:03  (17:21)
```

### 15. nohup

nohup stands for "No Hang Up". This allows to run command/process or shell script that can continue running in the background after you log out from a shell.

```bash 
nohup command

nohup command &
```


> **Refer:**

> [1]. https://github.com/Idnan/bash-guide

> [2]. [Linux的五个查找命令](http://www.ruanyifeng.com/blog/2009/10/5_ways_to_search_for_files_using_the_terminal.html)

> [3]. [25 simple examples of Linux find command](http://www.binarytides.com/linux-find-command-examples/)

> [4]. [The locate Command](http://www.linfo.org/locate.html)

> [5]. [10 Linux DIG Command Examples for DNS Lookup](http://www.thegeekstuff.com/2012/02/dig-command-examples/)
