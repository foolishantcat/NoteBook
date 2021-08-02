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



## git分支默认含义

- master：主分支，主要用来版本发布
- develop：日常开发分支，该分支正常保存了开发的最新代码
- feature：具体的功能开发分支，至于develop分支交互
- release：release分支可以认为是master分支的未测试版。比如说某一期的功能全部开发完成，那么久将develop分支合并到release分支，测试没有问题后，并且到了发布日期就合并到master分支，进行发布。
- hotfix：线上bug修复分支



## merge策略

> $ git checkout master 			# 进入某个分支
>
> $ git pull									# 拉取某个分支最新代码
>
> $ git merge release_xxxx		# 合并release_xxxx分支代码到master分支

分支合并，一般会自动解决一些可以自动合并的冲突，这取决于合并算法是否足够“智能”，当然，大部分情况是够用的，合并策略大致分为以下几种：

- resovle
- recursive
  - ours
  - theirs
  - patience
  - no-renames
  - 其他参数
- octopus
- ours
- subtree

### resovle

使用三路合并算法。**普通**的三路合并算法会存在发现多个共同祖先的问题。此策略会“仔细地”寻找其中一个共同祖先。

由于不需要递归合并出虚拟节点，所以次方法合并式会比较快速，但也可能会带来更多冲突。需要注意的是，自动合并成功并不一定意味着代码含义上也算是正确的合并。该策略会让更多的冲突变成手工合并而不是自动合并。

### recursive

**默认合并策略**，如果不指定策略参数，那么将使用这个合并策略。这将直接使用**递归**三路合并算法进行合并。

当指定为此策略时，可以额外指定下面的这些参数，方法是：

> $ git merge release_xxxx --strategy=recursive -X diff-algorithm=patience

包含的额外策略如下：

#### ours

如果不冲突，那么与默认的合并方式相同。如果发生冲突，将自动应用自己这一方面的修改。

注意额外策略里面也有一个ours，与这个不同。

#### theirs

这与ours相反。如果不冲突，那么与默认的合并方式相同。如果发生冲突，将自动应用来自其他人的修改（也就是merge参数中指定的那个分支的修改）。

#### patience

“耐心”策略，git将花费更多的时间来进行合并一些看起来不怎么重要的行，合并的结果也更加准确。

如果经常合并出现这些括号丢失或符号不再匹配的问题，可以考虑使用`patience`策略进行合并。

#### no-renames

默认情况下git会识别你重命名或者移动了文件，以便在你移动了文件之后依然可以与源文件进行合并。如果指定了此策略，那么git将不再识别重命名，而是当做增加和删除了文件。

#### 其他参数

- diff-algorithm=[patience|minimal|histogram|myers]
- renormalize
- no-renormalize
- find-renames[=\<n\>]
- rename-threshold=\<n\>
- subtree[=\<path\>]

### octopus

翻译为：章鱼。章鱼有很多触手，此合并策略就像这么多的触手一样。

此策略允许合并多个git提交节点（分支），不过，如果出现需要手工解决的冲突，那么此策略将不会执行。

该策略就是用来把多个分支聚集在一起。

### ours

在合并的时候，无论有多少个合并分支，当前分支就是最终的合并结果。无论其他人有多少修改，此合并之后，都将不存在，当然历史里面还有。

当你准备重新在你的仓库中进行开发（比如：重构），那么你的修改与旧分支合并式，采用此合并策略就非常有用，你新的重构代码将完全不会被旧分支的改动有所影响。

注意：recursive策略中也有一个ours参数，与这个不同的。

### subtree

此策略使用的是修改后的**递归**三路合并算法，与recursive不同的是，此策略会将合并的两个分支的其中一个视为另一个子树，就像git subtree中使用的子树一样。













