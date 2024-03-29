# sftp协议详解

日常工作中，有时候需要上传一些文件到服务器上面，假如文件数据量比较大，我们一般不会选择HTTP（超文本传输协议），因为http协议是应用层协议里面协议层约束最多的，这就表示它会浪费较多的网络带宽在传输协议本身上（比如header）。这个时候我们会选择比较轻量的sftp，那很多同学就会郁闷了，他们之间有什么区别呢？我们怎么选择通讯协议呢？接下来从TCP/IP协议开始讲起，逐个介绍他们之间的区别。

在此之前，让我们对整个网络层次有一个大概的了解：

TCP/IP通讯协议，采用了4层的层级结构，每一层都呼叫它的下一层所提供的网络来完成自己的需求，这4层分别为：

- 应用层；应用程序间沟通的层，如简单电子邮件传输（SMTP）、文件传输协议（FTP）、网络远程访问协议（Telnet）等。当然，应用层，可以进一步划分为：应用层、表示层、会话层。
- 传输层；在此层中，它提供了节点间的数据传送，应用程序之间的通信服务，主要功能是数据格式化、数据确认和丢失重传等。如传输控制协议（TCP）、用户数据报协议（UDP）等，TCP和UDP给数据包加入传输数据并把它传输到下一层中，这一层负责传送数据，因此，也被称为传输层，并且确定数据已被送达并接收。
- 网络层；负责提供基本的数据封包传送功能，让每一块数据包都能偶到达目的主机（但不检查是否被正确接收），如网际协议（IP）。
- 接口层（主机-网络层）；接收IP数据报并进行传输，从网络上接收物理帧，抽取IP数据报转交给下一层，对实际的网络媒体的管理，定义如何使用实际网络（如Ethernet、Serial Line等）来传送数据。当然网络接口层，还可以被细分为：数据链路层、物理层。

从上面的介绍我们可以知道：http协议是应用层协议，ftp和sftp也是。所以大部分我们的工作是围绕应用层展开的。当然也有更深层次一点的，比如面试的时候我们经常看到一个字眼：精通socket编程。这个socket套接字变成就是基于TCP/UDP协议的，这个是传输层协议的知识。

**FTP（File Transfer Proocol）：文件传输协议**；FTP是TCP/IP网络中最早使用的协议之一。相比于http协议，ftp协议结构上要复杂很多，ftp协议需要用到两个TCP连接，一个是命令链路，用来在客户端与服务器之间传递命令；另一个是数据链路，用来上传或下载数据。显然，FTP协议是基于TCP协议的。

FTP工作模式：

- PORT（主动模式）：客户端想服务器的FTP端口（默认是21）发送连接请求，服务器接受连接，建立一条命令链路。当需要传送数据时，客户端在命令链路上用PORT命令告诉服务器：**“我打开了1024+的随机端口，你过来连接我”**。于是服务器从20端口向客户端的1024+随机端口发送连接请求，建立一条数据链路来传送数据。如果客户端使用代理服务器，或者客户端防火墙被设置，都有可能会引起连接失败。
- PASV（Passive被动）：客户端向服务器的FTP端口（默认是21）发送连接请求，服务器接受连接，建立一条命令链路。当需要传送数据时，服务器在命令链路上用PASV命令告诉客户端：**“我打开了一个1024+的随机端口，你过来连接我”**。于是客户端向服务器的指定端口发送连接请求，建立一条数据链路来传送数据。因此，服务端防护墙除了要开放21端口外，还要开放PASV配置指定的端口范围。

**SFTP（Secure File Transfer Protocol）：安全文件传输协议**；sftp和ftp有着几乎一样的语法和功能。所以，通常我们可以认为他们没有太大区别。但是sftp时ssh协议的一部分，在ssh软件包中已经包含了一个叫做sftp的安全文件传输子系统，sftp本身并没有单独的守护进程（后台服务），它必须使用sshd守护进程（端口号默认是22）来完成相应的连接操作，所以，从某种意义上来说，sftp并不像一个服务器程序，更像一个客户端程序。sftp之所以安全可靠，是由于传输方式使用了加密/解密技术。从而，传输效率比普通的ftp要低得多。如果你对网络安全性要求更高，可以使用sftp替代ftp；反之则没有必要。

**SCP（Secure Copy）：安全拷贝**；scp是用来进行远程文件复制的，并且整个复制过程是加密的。数据传输使用的是ssh协议，并且使用和ssh同样的认证方式，提供同样的安全保证。

**SSH（Secure Shell）**：ssh为建立在应用层和传输层基础上的安全协议。专门为远程登陆会话和其他网络服务提供安全性的协议。利用ssh协议可以有效防止远程管理过程的信息泄漏问题。ssh是由客户端和服务端软件组成的：服务端只有一个守护进程（daemon），一般来说都是**sshd**进程，提供包括公共密钥认证、密钥交换、对称密钥加密和非安全连接；客户端包含ssh程序以及像scp、slogin、sftp等其他的应用程序。

从客户端看，ssh提供两种安全级别的安全验证：基于口令的安全验证（输入密码）；基于密钥的安全验证（使用密钥文件）。也正因为如此，当我们日常需要通过ssh协议进行登陆或者传输的场景下，输入密码的操作通常都可以利用可信的密钥替代（如：github）。

SSH主要由三部分组成：传输层协议（ssh-trans）；用户认证协议（ssh-userauth）；连接协议（ssh-connet）。

--------

# 配置sftp

以上我们基本上把sftp周边的协议讲清楚了，那么接下来我们需要开始配置和使用sftp了。

首先我们需要添加一个专用于sftp的用户组：

```shell
groupadd sftp
```

创建一个sftp账户：

```shell
useradd -g sftp -s /bin/bash testsftp
# 如果使用/sbin/nologin则创建的用户无法使用ssh登陆，也无法命令行切换用户的方式切换过去
# 不指定用户组，默认用户组就是用户名本身
useradd -d /home/testsftp -s /sbin/nologin testsftp
```

设置账号密码：

```shell
passwd testsftp
```

创建一个目录作为sftp根目录：

```shell
mkdir /var/testsftp/
```

<font color=red>这个目录不建议使用/home/testsftp用户目录</font>，因为我们并不希望用户通过这个账户登陆机器，设置home目录有泄漏风险。

设置目录权限：

```shell
chown -R root:sftp /var/testsftp/
chmod -R 755 /var/testsftp/
```

这里需要注意：

1. 根目录所有者被全部设置为**root（必要）**
2. 根目录所有组全部被设置为**sftp（非必要）**

填写必要是因为，sshd在启动的时候，必须要求文件夹具有所有者root属性，否则启动失败。

至于需要指定一个目录上传或者下载文件，我建议建立一个二级目录：

```shell
mkdir /var/testsftp/upload/
chown testsftp:root /var/testsftp/upload/
chmod u+rw /var/testsftp/upload/
```

配置sshd服务（sftp）：

配置文件地址：`/etc/ssh/sshd_config`

其实就是**sshd进程**的 配置文件。所以，我们在配置完sftp之后，ssh远程登陆的端口也会随之改变，通常默认端口是22，那么就需要在命令行显示指定**ssh -p port userid@ip**。

打开sshd_config文件，跳到最文件末尾，添加：

```shell
Subsystem sftp internal-sftp  # 指定sftp服务
Match User testsftp  # 匹配用户
ChrootDirectory /var/testsftp/  # 指定sftp根目录
```

启动sftp：

重启sshd服务即可，`sudo service sshd restart`

------

一般按照步骤来，服务已经可以重启了，sftp运行正常。

当然也会出现一些问题，比较常见的问题如下：

```shell
> Write failed: Broken pipe     
> Couldn't read packet: Connection reset by peer
这个问题的原因是ChrootDirectory的权限问题，你设定的目录必须是root用户所有，否则就会出现问题。所以请确保sftp用户根目录的所有人是root, 权限是 750 或者 755。注意以下两点原则：
目录开始一直往上到系统根目录为止的目录拥有者都只能是 root，用户组可以不是 root。
```

----------

通常来说，我们服务器会开放特定端口到外部，但通常都不包括sftp的端口，所以，我们需要使用一种比较折衷的办法来解决这个问题。即不暴露ssh服务端口，也要将数据通过sftp回传。

使用nginx反向代理sftp端口服务。

-------------

# know_hosts文件

我们在配置proftp的过程中，遇到个别机器无法登陆sftp的问题，报错如下：

```shell
~ » sftp -oPort=8080 ethanmac@192.168.1.213                                                                          255 ↵ ethancao@EthanCaodeMacBook-Pro
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:m3waO1sRGg7hLppTb+pLqIW/dwHR47MhMTaCWxsMuwE.
Please contact your system administrator.
Add correct host key in /Users/ethancao/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/ethancao/.ssh/known_hosts:4
RSA host key for [192.168.1.213]:8080 has changed and you have requested strict checking.
Host key verification failed.
Connection closed
```

这个错误主要是因为`know_hosts`文件记录了上一次访问该IP时所使用的公钥与本次所访问该IP的公钥不相同，所以就报错。

解决方案：

> 手动删除`know_hosts`文件里面对应IP所在的行即可
>
> 或者可以使用命令：ssh-keygen -R 192.168.1.213

参考文档：

> http://man.openbsd.org/sftp （sftp命令参数解析）
>
> http://man.openbsd.org/sshd_config.5 （sshd_config配置文件解析）





