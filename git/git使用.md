## git打tag

有时候上线一个版本后，出现故障了，需要紧急回顾，如果公司内部还没有成熟的代码回滚平台，那么可以使用打`tag`的方式，为上一个已经在线上运行的版本，打个标签。具体操作如下：

### 列出已有的tag

```shell
$ git tag
```

加上`-l`命令可以使用通配符来过滤tag

### 新建tag

使用`git tag`命令跟上tag名字，直接创建一个tag

```shell
$ git tag v1.0
```

上面创建一个名为`v1.0`的tag。使用`git tag`命令可以查看到新增的tag。

还可以加`-a`参数来创建一个带备注的tag，备注信息由`-m`指定。如果你未传入`-m`则创建过程系统会自动为你打开编辑器让你填写备注信息。

```shell
$ git tag -a tagName -m "my tag"
```

### 查看tag详细信息

`git show`命令可以查看tag的详细信息，包括commit号等

```shell
$ git show v1.0
```

### 给指定的某个commit号加上tag

打tag不必要在head之上，也可以在之前的版本上打，这需要你知道某个提交对象的校验和（`git log`获取，取校验和的前几位数字即可）

```shell
$ git tag -a v1.2 93hjk12d -m"my tag"
```

### 推送到远程服务器

同步提交代码后，使用`git push`来推送到远程服务器一样，`tag`也需要进行推送才能到远端服务器。

使用`git push origin [tagName]`推送单个tag

使用`git push origin --tags`推送本地所有tag

### 切换到某个tag

跟分支一样，可以直接切换到某个tag去。这个时候不位于任何分支，**处于游离状态**，可以考虑基于这个tag创建一个分支。

```shell
$ git tag
v1.0
v1.2

$ git checkout v1.0

```

### 删除某个tag

- 本地删除

```shell
$ git tag -d v1.0
```



- 远端删除

```shell
$ git push origin :refs/tags/v1.0
```

