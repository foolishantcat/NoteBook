# Scala开发须知

​	scala一般用于开发高并发高可用的网络后台程序，也可以用于开发spark程序。以下先介绍如何创建一个scala后台（命令行）程序需要的步骤。

## 开发环境搭建

- IDE：intelliJ IDEA community（社区版本）
- scala安装包
- sbt安装包
- jdk使用1.8就ok

以上包自行安装需要的版本



创建sbt工程：File-->New -->Project

![new_project](E:\webank_code\NoteBook\scala\new_project.png)

新建工程后会，生成的目录结构如下：

|--.idea（工程文件）

|--project（项目文件夹）

|--src（源代码目录）

​	|--main

​		|--scala（源码包放置在该目录下）

​	|--test（单元测试目录）

​		|--scala

|--build.sbt（工程构建文件）

当工程目录架构被创建之后，idea会根据build.sbt文件下载一系列需要的Libraries和Plugins，不够的需要自己添加。当然，也可以在sbt文件中定义一些其他的操作，以下是参数详解：

|              参数名 | 含义                             |
| ------------------: | -------------------------------- |
|                name | 项目名称                         |
|        organization | 组织名称                         |
|             version | 版本号                           |
|        scalaVersion | 使用的scala版本号                |
| libraryDependencies | 添加源码编译运行期间使用的依赖包 |
|                     |                                  |

除此之外，还需要在project目录下面新建一个文件：plugins.sbt，添加以下内容：

```sbt
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.14.7")
```

以上内容的作用是安装assembly打包模块。通常我们使用packge命令进行打包，但是引用第三方包的情况下，不会主动打包第三方包，造成编译通过，但是无法正确运行。提示：class 丢失

## 创建hello world

关于scala语法以及特性，请参考：[Scala开发教程]( https://www.w3cschool.cn/scaladevelopmentguide/zecg1jb8.html )

src/main/scala/test/Main.scala

```scala
package test

object Main {
  def main(args: Array[String]): Unit = {
  	println("hello world!")    
  }
}
```

- 初始化sbt环境

```shell
>sbt
[info] Loading global plugins from ***
[info] Loading settings for project ***-build from plugins.sbt ...
[info] Loading project definition from ****
[info] Loading settings for project test from build.sbt ...
[info] Set current project to test (in build file:***)
[info] sbt server started at local:sbt-server-72b704482cc3cfe0971e
```

- 清除

```shell
>clean
清除tarhget下生成的文件
```

- 更新

```shell
>update
根据构建配置更新依赖项
```

- test

```shell
>test
运行test目录下的所有测试用例
```

- reload

```shell
>reload
重新载入构建配置文件
```

- compile

```shell
>compile
编译项目，生成class文件
```

- package

```shell
>package
将src/main中的所有类打包为jar
```

- assembly（安装sbt-assembly插件才有）

```shell
>assembly
根据项目配置的libraryDependencies进行打包
```

