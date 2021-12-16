# Shell小笔记

用于记录一下运维的shell小知识



## 删除乱码文件

删除各种???乱码文件

```shell
find /data/ethan/DSP/bin ! -name "[a-z,A-Z]*"  | awk -F "/" '$NF != ""{print}' | xargs rm -fr
```

字符串运算

| 运算符 | 说明                                      | 举例                     |
| :----- | :---------------------------------------- | :----------------------- |
| =      | 检测两个字符串是否相等，相等返回 true。   | [ $a = $b ] 返回 false。 |
| !=     | 检测两个字符串是否相等，不相等返回 true。 | [ $a != $b ] 返回 true。 |
| -z     | 检测字符串长度是否为0，为0返回 true。     | [ -z $a ] 返回 false。   |
| -n     | 检测字符串长度是否为0，不为0返回 true。   | [ -n "$a" ] 返回 true。  |
| $      | 检测字符串是否为空，不为空返回 true。     | [ $a ] 返回 true。       |

注意：字符串运算，空格虽然不现实，但是占用字符串长度

去除空格：

```shell
$echo "a b_c d" | sed 's/ //g'
ab_cd
```



## 如何快速找出进程并kill

```shell
ps -ef | grep gdb | grep -v grep | awk '{print $2}' | sudo xargs kill -9 
```



## tar简单使用

tar包的创建

```shell
tar -cvf file.tar file1 {file2}
tar -zcvf file.tar.gz file1 {file2}
tar -jcvf file.tar.bz2 file1 {file2}
```

tar包的查看

```shell
tar -tvf file.tar
tar -ztvf file.tar.gz
tar -jtvf file.bar.bz2
```

释放tar包

```shell
tar -xvf file.tar
tar -zxvf file.tar.gz
tar -jxvf file.tar.bz2
```

打包一个文件夹，但是排除某（几）个文件

```shell
tar -zcvf test.tar.gz --exclude=test/1 test
```



## fuser

fuser命令是用来显示所有正在使用着指定的file、file system或者sockets的进程信息。

- 返回值

fuser如果没有找到任何进程正在使用指定的file、file system或sockets，或者在查找过程中发生了fatal error，则返回non-zero值

fuser如果找到至少一个进程正在使用指定的file、file system或sockets，则返回zero（0）

- 使用场景

fuser通常被用在诊断系统的“resource busy”问题，通常是在你希望umount指定的挂载点的时候雨大。如果你希望kill所有正在使用某一特定的file、file system Or sockets的进程的时候，你可以使用`-k`选项。

```shell
fuser -k /path/to/your/filename
```

这时，fuser会向所有正在使用`path/to/your/filename`的进程发送`SIGKILL`。如果你希望在发送之前得到提示，可以使用`-i`选项。

```shell
fuser -k -i /path/to/your/filename
```

另外，在实际应用工作的过程中，我们还使用fuser来观察是否某个服务已经正确启动，这时我们会使用`-s`选项。

```shell
fuser -s $TCP_PORT/tcp > /dev/null 2>&1
return $?
```

这里，`-s`表示静默执行，不打印执行结果，这样不会在启动日志里面留下多余的日志，该命令，以返回zero（0）表示正常启动并绑定了TCP的端口。



## shell交互式输入

shell中有时我们需要交互，但是呢又不想每次从stdin输入，想让其自动化，这时我们就要使shell交互输入自动化了。

- 使用read重定向

```shell
#! /bin/bash
read -p "enter number:" no
read -p "enter name:" name
echo you hava entered ${no}, ${name}
```

- 利用管道完成交互的自动化

```shell
$ echo -e "xxx" | ./test.sh
```

这种办法看起来和直接带参数输入没什么区别

- 利用expect

expect是专门用来交互自动化的工具，但它有可能不是随系统就安装好的，有时需要自己手工安装该命令。所以这里不作过多介绍。



## shell变量作用域

shell变量分为：**全局变量、环境变量、局部变量**，这点和C语言很相似。

- 局部变量，只能在函数内部使用
- 全局变量，可以在当前shell进程中使用
- 环境变量，可以在子进程中使用

**shell局部变量：**

shell支持自定义函数，但是shell函数和C++、Java、C#等其他编程语言函数的一个不同点就是：**在shell函数中定义的变量默认也是全局变量**，它和在函数外部定义变量拥有一样的效果：

```shell
#! /bin/bash
function func() {
	a=99
}

func

echo ${a}
```

输出结果：

> 99

想要变量的作用域仅限于函数内部，可以在定义时加上`local`命令，此时该变量就成了局部变量。

**shell环境变量：**

全局变量只有当前shell进程中有效，对其他shell进程和子进程都无效。如果使用`export`命令将全局变量导出，那么它就在所有的子进程中也有效了，这称为“环境变量”。

注意：没有父子关系shell进程是不能传递环境变量的，并且环境变量只能向下传递，而不能向上传递，即“传子不传父”。

创建shell子进程最简单的方式是运行`bash`命令。

```shell
$ bash
$  (此处已经进入了shell子进程)
```

通过`exit`命令可以一层一层地退出shell。

注意：通过export导出的环境变量，只对当前shell进程以及所有的子进程有效，如果最顶层的父进程被关闭，那额环境变量也就随之消失了，其他进程也就无法使用了，所以说环境变量也是临时的。

如果想要一个变量在所有的shell进程中都有效，不管他们之间是否存在父子关系，那么最简单的办法就是配置shell，shell进程每次启动都会执行配置文件中的代码做一些初始化工作，那么每次启动进程都会定义这个变量。


