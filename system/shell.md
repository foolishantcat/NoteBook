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