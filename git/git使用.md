git打tag

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



### git查看某个文件的修改记录

```shell
git log {filename}
```

可以看到filename相关的commit记录

```shell
git log -p {filename}
```

可以显示每次提交的`diff`

```shell
git show {commitid} {filename}
```

可以查看某次提交中的某个文件变化



## stash使用

**前提：必须是出于git下的文件，未add到git的文件无法使用**

`git stash`这条命令主要用于当前的修改并没有`git add`到暂存区，并且希望可以`git checkout`到其它分支。

- `git stash`

保存当前工作进度，并且将`工作区`和`暂存区`恢复到修改之前。

- `git stash save {message}`

作用同上，message为此次进度保存的说明。

- `git stash list`

显示保存的工作进度列表，编号越小代表保存进度的时间越近

- `git stash pop stash@{num}`

恢复工作进度到工作区，次命令的`shash@{num}`是可选项，在多个工作进度中可以选择恢复，不带此项默认恢复最近的一次进度

相当于`git stash pop stash@{0}`

- `git stash apply stash@{num}`

恢复工作进度到工作区且该工作进度可重复恢复，此命令的`stash@{num}`是可选项，在多个工作进度中可以选择恢复，不带此项则默认恢复最近的异常进度，相当于`git stash apply stash@{0}`

- `git stash drop stash@{num}`

删除一条保存的工作进度，此命令的`stash@{num}`是可选项，在多个工作进度中可以选择删除，不带此项则默认删除最近的一次进度

相当于`git stash drop stash@{0}`

- `git stash clear`

删除所有保存的工作进度