# ping


### ping命令
```bash
~ ping leohowell.com
PING leohowell.com (163.44.169.240): 56 data bytes
64 bytes from 163.44.169.240: icmp_seq=0 ttl=49 time=105.235 ms
64 bytes from 163.44.169.240: icmp_seq=1 ttl=49 time=105.982 ms
64 bytes from 163.44.169.240: icmp_seq=2 ttl=49 time=106.013 ms
64 bytes from 163.44.169.240: icmp_seq=3 ttl=49 time=105.903 ms
64 bytes from 163.44.169.240: icmp_seq=4 ttl=49 time=105.904 ms
^C
--- leohowell.com ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 105.235/105.807/106.013/0.289 ms
```

### Flood ping

我在动态迁移虚拟机时使用过，在不同的hypervisor上迁移虚拟机，同时保证IP不发生变化，并且迁移过程中虚拟机保持可用。

>Flood ping. For every ECHO_REQUEST sent a period ``.'' is printed, while for ever ECHO_REPLY received a backspace is printed.  This provides a rapid display of  how  many  packets  are
> being  dropped.   If  interval is not given, it sets interval to zero and outputs packets as fast as they come back or one hundred times per second, whichever is more.  Only the super-
> user may use this option with zero interval.

```bash
ping -f leohowell.com
PING leohowell.com (163.44.169.240) 56(84) bytes of data.
.............................................................................^C
--- leohowell.com ping statistics ---
1908 packets transmitted, 1626 received, 14% packet loss, time 24226ms
rtt min/avg/max/mdev = 104.536/106.162/173.870/3.156 ms, pipe 15, ipg/ewma 12.703/106.072 ms
```

### 监听icmp-echo消息

```bash
sudo tcpdump -i eth0 icmp and icmp[icmptype]=icmp-echo
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
18:48:14.172454 IP bogon > bogon: ICMP echo request, id 59424, seq 0, length 64
18:48:15.174358 IP bogon > bogon: ICMP echo request, id 59424, seq 1, length 64
18:48:16.174460 IP bogon > bogon: ICMP echo request, id 59424, seq 2, length 64
18:48:17.175342 IP bogon > bogon: ICMP echo request, id 59424, seq 3, length 64
^C
4 packets captured
5 packets received by filter
0 packets dropped by kernel
```

### 通过scapy模拟ping命令

```bash
scapy
 Welcome to Scapy (2.3.3)
```

```python
>>> icmp_packet = IP(dst="192.168.1.1")/ICMP()
>>> icmp_packet.show()
###[ IP ]###
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags=
  frag= 0
  ttl= 64
  proto= icmp
  chksum= None
  src= 192.168.2.153
  dst= 192.168.1.1
  \options\
###[ ICMP ]###
     type= echo-request
     code= 0
     chksum= None
     id= 0x0
     seq= 0x0
>>> send(imcp_packet)
.
Sent 1 packets.
>>>
```

### 关于ICMP

>网络控制消息协定（英文：Internet Control Message Protocol，ICMP）是网路协议族的核心协议之一。它用于TCP/IP网络中发送控制消息，提供可能发生在通信环境中的各种问题反馈，通过这些信息，令管理者可以对所发生的问题作出诊断，然后采取适当的措施解决。

>ICMP依靠IP来完成它的任务，它是IP的主要部分。它与传输协议，如TCP和UDP显著不同：它一般不用于在两点间传输数据。它通常不由网络程序直接使用，除了ping和traceroute这两个特别的例子。 IPv4中的ICMP被称作ICMPv4，IPv6中的ICMP则被称作ICMPv6。

> --[维基百科](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%8E%A7%E5%88%B6%E6%B6%88%E6%81%AF%E5%8D%8F%E8%AE%AE)
