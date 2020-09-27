# Mac使用技巧

## 命令行工具

### netstat

netstat的使用方式不同于Linux，一般来说我们输入

```shell
$ netstat -nlp | grep 'PORT'
```

来查询端口信息。

mac貌似-p参数需要带上协议簇才可以使用

```shell
$ netstat -nlp tcp | grep 'PORT'
```

### brew

以下内容摘自：https://zhuanlan.zhihu.com/p/59805070

brew貌似macOS10.x没有自带，需要自行安装

```shell
$ curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install >> brew_install
$ /usr/bin/ruby brew_install
```

同理卸载脚本

```shell
$ curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall >> brew_uninstall
$ /usr/bin/ruby brew_uninstall
```

这种方式安装brew需要耗费很长时间，那是因为软件源在国外

**所以接下来，我们替换为国内软件源**

```shell
$ vim brew_install
```

把以下两句注释掉

```shell
BREW_REPO = “https://github.com/Homebrew/brew“.freeze
CORE_TAP_REPO = “https://github.com/Homebrew/homebrew-core“.freeze
```

修改为

```shell
BREW_REPO = "git://mirrors.ustc.edu.cn/brew.git".freeze
CORE_TAP_REPO = "git://mirrors.ustc.edu.cn/homebrew-core.git".freeze
```

但是实际上，我只看到`BREW_REPO`

接下来我们再执行安装操作

```shell
$ /usr/bin/ruby brew_install
```

之后你会看到执行失败了

```shell
==> Homebrew is run entirely by unpaid volunteers. Please consider donating:
  https://github.com/Homebrew/brew#donations
==> Tapping homebrew/core
Cloning into '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (9/9), done.
error: RPC failed; curl 18 transfer closed with outstanding read data remaining
fatal: the remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed
Error: Failure while executing; `git clone https://github.com/Homebrew/homebrew-core /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core` exited with 128.
Error: Failure while executing; `/usr/local/bin/brew tap homebrew/core` exited with 1.
Failed during: /usr/local/bin/brew update --force
```

原因还是因为源地址不对，我们直接用国内源替换进行下载

```shell
$ git clone git://mirrors.ustc.edu.cn/homebrew-core.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core --depth=1
```

可以看到，homebrew-core已经下载成功了，接下来我们将homebrew-core的源地址替换掉

```shell
$ cd "$(brew --repo)"
$ git remote set-url origin https://mirrors.ustc.edu.cn/brew.git
$ cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
$ git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
```

执行更新brew

```shell
$ brew update
```

接着又执行brew检测命令

```shell
$ brew doctor
```

```shell
Please note that these warnings are just used to help the Homebrew maintainers
with debugging if you file an issue. If everything you use Homebrew for is
working fine: please don't worry or file an issue; just ignore this. Thanks!

Warning: Suspicious https://github.com/Homebrew/brew git origin remote found.
The current git origin is:
  https://mirrors.ustc.edu.cn/brew.git

With a non-standard origin, Homebrew won't update properly.
You can solve this by setting the origin remote:
  git -C "/usr/local/Homebrew" remote set-url origin https://github.com/Homebrew/brew

Warning: Suspicious https://github.com/Homebrew/homebrew-core git origin remote found.
The current git origin is:
  https://mirrors.ustc.edu.cn/homebrew-core.git

With a non-standard origin, Homebrew won't update properly.
You can solve this by setting the origin remote:
  git -C "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core" remote set-url origin https://github.com/Homebrew/homebrew-core

Warning: "config" scripts exist outside your system or Homebrew directories.
`./configure` scripts often look for *-config scripts to determine if
software packages are installed, and which additional flags to use when
compiling and linking.

Having additional scripts in your path can confuse software installed via
Homebrew if the config script overrides a system or Homebrew-provided
script of the same name. We found the following "config" scripts:
  /Library/Frameworks/Python.framework/Versions/3.8/bin/python3-config
  /Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8-config
```

会出现一些warning，这都是正常的，毕竟我们替换掉了源地址

如上面出现警告是正常情况，因为我们更改了镜像源

到目前为止，海外用户或者已经设置系统全局代理的用户就可以使用brew安装你所需要的软件了

国内用户咱们继续操作，不然龟速下载搞得我想摔电脑！

让我们把默认源替换成国内USTC源

- 替换核心软件仓库

```shell
$ cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
$ git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
```

- 替换cask软件仓库

在此之前我们需要先安装cask

```shell
$ git clone git://mirrors.ustc.edu.cn/homebrew-cask.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask --depth=1
```

替换cask源

```shell
$ cd "$(brew --repo)"/Library/Taps/homebrew/homebrew-cask
$ git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git
```

- 替换Bottel源（最后这一步我不不太理解干嘛用）

bash用户（shell用户）

```shell
$ echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
$ source ~/.bash_profile
```

zsh用户

```shell
$ echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
$ source ~/.zshrc
```

接下来就可以正常使用brew了

我们可以看到在/usr/local目录下面生成了很多子目录

```shell
drwxrwxr-x   2 ethancao  admin   64  2 21 18:58 Caskroom
drwxrwxr-x   4 ethancao  admin  128  2 21 19:46 Cellar
drwxrwxr-x   3 ethancao  admin   96  2 21 19:46 Frameworks
drwxrwxr-x  20 ethancao  admin  640  2 21 19:46 Homebrew
drwxrwxr-x   5 ethancao  admin  160  2 21 19:46 bin
drwxrwxr-x   3 ethancao  admin   96  2 21 19:46 etc
drwxrwxr-x   3 ethancao  admin   96  2 21 19:46 include
drwxrwxr-x   3 ethancao  admin   96  2 21 19:46 lib
drwxrwxr-x   4 ethancao  admin  128  2 21 19:46 opt
drwxrwxr-x   3 ethancao  admin   96  2 21 19:46 sbin
drwxrwxr-x   5 ethancao  admin  160  2 21 19:46 share
drwxrwxr-x   3 ethancao  admin   96  2 21 18:58 var
```



### telnet

telnet也没有自定义安装的情况下，假如安装了brew，可以通过如下方式安装

```shell
$ brew install telnet
```

### maven

配置maven镜像可以让下载jar包的速度大大提升，我亲测使用aliyun的镜像可用

```text
Apache Maven 3.6.3
Java version: 1.8.0_231, vendor: Oracle Corporation, runtime: /Library/Java/JavaVirtualMachines/jdk1.8.0_231.jdk/Contents/Home/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "mac os x", version: "10.15.2", arch: "x86_64", family: "mac"
```

修改maven镜像地址

```shell
cd apache-maven-3.6.3/conf/
vim settings.xml
```

在<mirrors></mirrors>中间添加以下内容：

```xml
<mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>*</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public</url>
</mirror>
```

使用maven编译和打包一下，发现sou的一下飞快～～

### open

直接在命令行使用open可以打开文件

```shell
$ open test.md
```

### nc

nc是netcat的简写

简单的使用方法，测试端口是否可用，配合telnet使用

```shell
$ nc -l 9090
# 另外开一个termimal
$ telnet localhost 9090
```

将收到的内容写入文件

```shell
$ nc -l 9090 > receive.tar.gz
```

作为源主机发起请求

```shell
$ nc 192.168.0.13 < receive.tar.gz
```

除此之外，nc还可以实现

```text
（1）实现任意TCP/UDP端口的侦听，nc可以作为server以TCP或UDP方式侦听指定端口
（2）端口的扫描，nc可以作为client发起TCP或UDP连接
（3）机器之间传输文件
（4）机器之间网络测速
```

其他参数说明

```text
1) -l
用于指定nc将处于侦听模式。指定该参数，则意味着nc被当作server，侦听并接受连接，而非向其它地址发起连接。
2) -p <port>
暂未用到（老版本的nc可能需要在端口号前加-p参数，下面测试环境是centos6.6，nc版本是nc-1.84，未用到-p参数）
3) -s 
指定发送数据的源IP地址，适用于多网卡机 
4) -u
 指定nc使用UDP协议，默认为TCP
5) -v
输出交互或出错信息，新手调试时尤为有用
6）-w
超时秒数，后面跟数字 
7）-z
表示zero，表示扫描时不发送任何数据
```

### ditto

当我们从windows拷贝一些中文字符的压缩文件（如zip）到mac下面的时候，unzip解压会出现类似下面的错误：

```shell
checkdir error:  cannot create work/????+-+?
                 Illegal byte sequence
                 unable to process ????+-+?/00.1-+???+???+??+ͩ-?(1).md.
```

这是由于文件名编码不同导致的，我们可以这样

```shell
$ ditto -V -x -k --sequesterRsrc 办公文件.zip work
```

### find & xargs

用于查找文件，并批量操作，和Linux命令行下面，略有区别

```shell
find ./target/generated-sources/ -name "*.java" | xargs  -n1 -I F cp "F" ./src/main/java/com/grpc/mistra/generate/ 
```

你品，你细品，这个命令真奇怪，好累赘的感觉，哈哈。

- 使用find查找文件夹/文件，并统计数量

```shell
find . -type f  | wc -l    # 统计当前目录下面所有文件，find递归
find . -type d  | wc -l    # 统计当前目录下面所有文件夹，find递归
```





## Vim使用

将vim中的内容全文拷贝到外部：

```shell
:%w !pbcopy
```



## Fish的使用

如果你觉得Mac自带的shell不太好用，或者不够炫，那么你肯定要装一个新东西了。**`fish`**

```shell
brew install fish
```

开启美的体验

但是有言在先，fish shell，和bash shell的兼容性不太好。