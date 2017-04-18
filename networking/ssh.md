# SSH (Secure Shell)

```bash
~ ssh -v root@192.168.2.153
OpenSSH_7.4p1, LibreSSL 2.5.0
debug1: Reading configuration data /Users/howell/.ssh/config
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Connecting to 192.168.2.153 [192.168.2.153] port 22.
debug1: Connection established.
debug1: identity file /Users/howell/.ssh/id_rsa type 1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_rsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_dsa type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_dsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_ecdsa type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_ecdsa-cert type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_ed25519 type -1
debug1: key_load_public: No such file or directory
debug1: identity file /Users/howell/.ssh/id_ed25519-cert type -1
debug1: Enabling compatibility mode for protocol 2.0
debug1: Local version string SSH-2.0-OpenSSH_7.4
debug1: Remote protocol version 2.0, remote software version OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.7
debug1: match: OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.7 pat OpenSSH_6.6.1* compat 0x04000000
debug1: Authenticating to 192.168.2.153:22 as 'root'
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: curve25519-sha256@libssh.org
debug1: kex: host key algorithm: ecdsa-sha2-nistp256
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: Server host key: ecdsa-sha2-nistp256 SHA256:/GQ1vXT8Kbg4B5fZ2oyjinF8BsHbD6xZQYGCYLwL5oQ
debug1: Host '192.168.2.153' is known and matches the ECDSA host key.
debug1: Found key in /Users/howell/.ssh/known_hosts:65
debug1: rekey after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey after 134217728 blocks
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering RSA public key: /Users/howell/.ssh/id_rsa
debug1: Server accepts key: pkalg ssh-rsa blen 279
debug1: Authentication succeeded (publickey).
Authenticated to 192.168.2.153 ([192.168.2.153]:22).
debug1: channel 0: new [client-session]
debug1: Requesting no-more-sessions@openssh.com
debug1: Entering interactive session.
debug1: pledge: network
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-31-generic x86_64)
```

### 迪菲-赫尔曼密钥交换 Diffie–Hellman key exchange (D-H)

选定素数p=23与原根g=6 (p, g均公开)

假定alice与bob进行交换

1. alice生成秘密整数a=5 `A = g ** a % p = 8` 并发送A至bob
2. bob生成秘密整数b=15 `B = g ** b % p = 15` 并发送B至alice
3. alice `s1 = B ** a % p = 2`
4. bob `s2 = A ** b % p = 2`    
5. s1 = s2

这是s1/s2可作为对称加密的key，并且s1/s2只有alice和bob知道

该算法被认为是窃听安全的，但是协商过程容易受到中间人攻击(通过添加身份验证解决)


### SSH连接过程

1. 建立对称加密连接阶段
    1. TCP连接建立之后，server发送给client可以接受的协议版本, client根据协议版本建立连接，server同时提供publish host key
    2. 通过Diffie-Hellman算法协商session key, 这个session 用来加密整个ssh会话过程
2. 认证阶段(根据SSH server接受的认证方式，简述一下password与ssh key pairs方式)
    1. password的传输虽然会被加密，但是由于密码本身复杂程度不一，容易被暴力破解，因而不被推荐
    2. ssh key pairs是被推荐的方式，公钥用来加密数据而且只能被私钥解密
        1. client发送id至server，server检查authorized_keys中是否有该账户对应的id, 没有则认证失败
        2. server生成一个随机数并使用对应账户的public key对该随机数进行加密，然后将加密消息发至client
        3. 如果client有对应私钥, 那么解密消息得到随机数, 并使用session key加密改随机数，然后计算MD5(或使用其他hash算法), 发送至server
        4. server用同样的方法计算MD5, 如果相同则认证通过

<br><br>
> 参考 <br>
> [1]. http://erik-2-blog.logdown.com/posts/74081-ssh-principle <br>
> [2]. https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process <br>
> [3]. https://zh.wikipedia.org/wiki/%E8%BF%AA%E8%8F%B2-%E8%B5%AB%E7%88%BE%E6%9B%BC%E5%AF%86%E9%91%B0%E4%BA%A4%E6%8F%9B <br>
