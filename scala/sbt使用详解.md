# SBT使用详解

## 安装（Installing）

- 安装jdk8+

- 安装sbt

Mac安装方法

```shell
$ brew install sbt
```

Win安装方法：比较推荐使用msi installer进行安装

安装版本：选择需要版本即可（推荐当前最新版本安装）

## 例子（Example）

```shell
$ mkdir foo-build
$ cd foo-build
$ touch build.sbt
```

### 启动sbt

```shell
$ sbt
[info] Updated file E:\webank_code\foo-build\project\build.properties: set sbt.version to 1.2.8
[info] Loading global plugins from C:\Users\home\.sbt\1.0\plugins
[info] Updating ProjectRef(uri("file:/C:/Users/home/.sbt/1.0/plugins/"), "global-plugins")...
[info] Done updating.
[info] Loading project definition from E:\webank_code\foo-build\project
[info] Updating ProjectRef(uri("file:/E:/webank_code/foo-build/project/"), "foo-build-build")...
[info] Done updating.
[info] Loading settings for project foo-build from build.sbt ...
[info] Set current project to foo-build (in build file:/E:/webank_code/foo-build/)
[info] sbt server started at local:sbt-server-93344f37fdf2bc3d506b
sbt:foo-build>
```

这个时候将生成两个文件夹：

```shell
foo-build/project/
foo-build/target/
```

这两个文件夹是sbt基础插件`plugins`生成的，你可以从`${HOME}/.sbt/1.0/plugins`下面看到这些插件

### 编译

```shell
$ sbt:foo-build> compile
[info] Updating ...
[info] Done updating.
[success] Total time: 1 s, completed 2020-2-26 11:30:14
```

创建源文件: `src/main/scala/example/Hello.scala`

```scala
package example

object Hello extends App {
  println("Hello")
}
```

自动编译功能

```shell
$ sbt:foo-build> ~compile
[success] Total time: 0 s, completed 2020-2-26 11:51:59
1. Waiting for source changes in project foo-build... (press enter to interrupt)
[info] Compiling 1 Scala source to E:\webank_code\foo-build\target\scala-2.12\classes ...
[info] Done compiling.
```

该功能的主要作用就是每当更新任意一个文件，将会触发`compile`

### 运行代码

```shell
$ sbt:foo-build> run
[info] Packaging E:\webank_code\foo-build\target\scala-2.12\foo-build_2.12-0.1.0-SNAPSHOT.jar ...
[info] Done packaging.
[info] Running example.Hello
Hello
[success] Total time: 1 s, completed 2020-2-26 11:54:58
```

保存当前sbt临时会话到`build.sbt`文件

```shell
$ sbt:foo-build> set ThisBuild / scalaVersion := "2.12.7"
[info] Defining ThisBuild / scalaVersion
```

```shell
$ sbt:foo-build> scalaVersion
[info] 2.12.7
```

```shell
$ sbt:foo-build> session save
[info] Reapplying settings...
[info] Set current project to foo-build (in build file:/E:/webank_code/foo-build/)
sbt:foo-build>
```

使用`build.sbt`给工程命名

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

lazy val hello = (project in file("."))
  .settings(
    name := "Hello"
  )
```

重新加载`build.sbt`文件

```shell
$ sbt:foo-build> reload
[info] Loading global plugins from C:\Users\home\.sbt\1.0\plugins
[info] Loading project definition from E:\webank_code\foo-build\project
[info] Loading settings for project hello from build.sbt ...
[info] Set current project to Hello (in build file:/E:/webank_code/foo-build/)
$ sbt:Hello>
```

可以看到提示行项目名称已经变更为`Hello`

接下来，我们也许需要为项目添加依赖的jar库，编辑`build.sbt`，我们这里使用`test`库

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

lazy val hello = (project in file("."))
  .settings(
    name := "Hello",
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % Test,
  )
```

执行`reload`

运行测试用例

```shell
$ sbt:Hello> test
[info] Updating ...
[info] Done updating.
[info] Run completed in 27 milliseconds.
[info] Total number of tests run: 0
[info] Suites: completed 0, aborted 0
[info] Tests: succeeded 0, failed 0, canceled 0, ignored 0, pending 0
[info] No tests were executed.
[success] Total time: 2 s, completed 2020-2-26 12:53:28
```

### 测试

接下来，可以尝试编写一个测试用例

`src/test/scala/HelloSpec.scala`

```scala
import org.scalatest._

class HelloSpec extends FunSuite with DiagrammedAssertions {
  test("Hello should start with H") {
    assert("hello".startsWith("H"))
  }
}
```

```shell
$ sbt:Hello> test
[info] HelloSpec:
[info] - Hello should start with H *** FAILED ***
[info]   assert("hello".startsWith("H"))
[info]          |       |          |
[info]          "hello" false      "H" (HelloSpec.scala:5)
[info] Run completed in 212 milliseconds.
[info] Total number of tests run: 1
[info] Suites: completed 1, aborted 0
[info] Tests: succeeded 0, failed 1, canceled 0, ignored 0, pending 0
[info] *** 1 TEST FAILED ***
[error] Failed tests:
[error]         HelloSpec
[error] (Test / test) sbt.TestsFailedException: Tests unsuccessful
[error] Total time: 1 s, completed 2020-2-26 12:58:37
```

### 子项目

我们还可以为当前项目添加一个子项目

修改`build.sbt`

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

lazy val hello = (project in file("."))
  .settings(
    name := "Hello",
    libraryDependencies += "com.eed3si9n" %% "gigahorse-okhttp" % "0.3.1",
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % Test,
  )

lazy val helloCore = (project in file("core"))
  .settings(
    name := "Hello Core",
  )
```

当下可以使用`projects`来查看有几个项目

```shell
$ sbt:Hello> projects
[info] In file:/E:/webank_code/foo-build/
[info]   * hello
[info]     helloCore
```

还可以使用命令行单独编译子项目

```shell
$ sbt:Hello> helloCore/compile
[info] Updating helloCore...
[info] Done updating.
[success] Total time: 0 s, completed 2020-2-26 13:03:29
```

可以挑出来一些公共依赖，并单独引用它们

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

val scalaTest = "org.scalatest" %% "scalatest" % "3.0.5"

lazy val hello = (project in file("."))
  .settings(
    name := "Hello",
    libraryDependencies += "com.eed3si9n" %% "gigahorse-okhttp" % "0.3.1",
    libraryDependencies += scalaTest % Test,
  )

lazy val helloCore = (project in file("core"))
  .settings(
    name := "Hello Core",
    libraryDependencies += scalaTest % Test,
  )
```

父子项目可以嵌套调用，也叫做命令广播`aggregate`， 这样对父项目执行的操作都会广播到子项目同时执行

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

val scalaTest = "org.scalatest" %% "scalatest" % "3.0.5"

lazy val hello = (project in file("."))
  .aggregate(helloCore)
  .settings(
    name := "Hello",
    libraryDependencies += "com.eed3si9n" %% "gigahorse-okhttp" % "0.3.1",
    libraryDependencies += scalaTest % Test,
  )

lazy val helloCore = (project in file("core"))
  .settings(
    name := "Hello Core",
    libraryDependencies += scalaTest % Test,
  )
```

还有一种情况是父项目依赖子项目，可以使用`dependsOn`

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

val scalaTest = "org.scalatest" %% "scalatest" % "3.0.5"

lazy val hello = (project in file("."))
  .aggregate(helloCore)
  .dependsOn(helloCore)
  .settings(
    name := "Hello",
    libraryDependencies += scalaTest % Test,
  )

lazy val helloCore = (project in file("core"))
  .settings(
    name := "Hello Core",
    libraryDependencies += "com.eed3si9n" %% "gigahorse-okhttp" % "0.3.1",
    libraryDependencies += scalaTest % Test,
  )
```

接下来添加插件`plugin`，插件的主要作用就是执行除标准动作（如：compile）之外的其他动作（如：assembly）

这需要我们额外创建一个`plugins.sbt`文件，当然文件命名可以是自定义的，也可以拆开写在多个文件里面，但是都必须要放在`project/`目录下

这里我们尝试添加一个打包依赖并在`build.sbt`中启用这个依赖`JavaAppPackaging`

```scala
ThisBuild / scalaVersion := "2.12.7"
ThisBuild / organization := "com.example"

val scalaTest = "org.scalatest" %% "scalatest" % "3.0.5"
val gigahorse = "com.eed3si9n" %% "gigahorse-okhttp" % "0.3.1"
val playJson  = "com.typesafe.play" %% "play-json" % "2.6.9"

lazy val hello = (project in file("."))
  .aggregate(helloCore)
  .dependsOn(helloCore)
  .enablePlugins(JavaAppPackaging)
  .settings(
    name := "Hello",
    libraryDependencies += scalaTest % Test,
  )

lazy val helloCore = (project in file("core"))
  .settings(
    name := "Hello Core",
    libraryDependencies ++= Seq(gigahorse, playJson),
    libraryDependencies += scalaTest % Test,
  )
```

运行`dist`进行打包，当然具体命令要取决于依赖组件的要求，但是通常来说我们不会使用该工具进行打包操作，所以这里不做详细论述了。

此外，还可以以添加插件的形式，增加直接使用sbt发布jar包到docker的功能，这里也不尽详述了。因为，这些五花八门的功能实际工作中我们使用的很少。

### 退出sbt

```shell
sbt:foo-build> exit
```

此外，值得着重介绍的依赖和插件，下文还有补充。

## 依赖（Dependency）

依赖可以通过两种方式添加：

- `unmanaged dependencies`未管理的依赖，被放置在`lib/`目录
- `managed dependencies`管理的依赖，自动从`repositories`下载

### Unmanaged dependencies

未管理的依赖模式，更加易于初学者开始，这是我要说的。

所以，只简单介绍如何自定义为管理依赖模式的jar库地址

```scala
unmanagedBase := baseDirectory.value / "custom_lib"
```

### Managed Dependencies

通常来说，正常的项目，我们都会使用管理依赖模式，所以下面详细说一下。

#### 声明

如何声明一个依赖？有两种方式

```scala
libraryDependencies += groupID % artifactID % revision
```

和

```scala
libraryDependencies += groupID % artifactID % revision % configuration
```

其中：`groupId`, `artifactId`, and `revision` 都是字符串，`configuration` 可以是一个字符串，或者也可以是一个经过配置的值 (如：`Test`)

还可以一次性定义一个依赖列表

```scala
libraryDependencies ++= Seq(
  groupID % artifactID % revision,
  groupID % otherID % otherRevision
)
```

我们可以看到，连接符是`%`，但是有时候我们也可以看到有的地方使用`%%`，区别是什么呢？

使用`%%`会自动在artifactId后面接上当前scala的版本，如：

```scala
libraryDependencies += "org.scala-tools" %% "scala-stm" % "0.3"
```

如果使用scala版本为2.11，等同于：

```scala
libraryDependencies += "org.scala-tools" % "scala-stm_2.11" % "0.3"
```

#### 下载

依赖库除开`unmanaged`模式，若不是手动拷贝进去目标文件夹（当然这也太low了），都是通过在线下载的方式来获取依赖jar包的。

但是值得注意的是，系统给我们配置了sbt默认下载地址，标准的`Maven2`库地址。假如你的依赖不是默认库地址，你可以通过`resolver`使得`lvy`找到正确的库地址。

格式如下：

```scala
resolvers += name at location
```

举例：

```scala
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
```

也可以配置为本地maven库

```scala
resolvers += "Local Maven Repository" at "file://"+Path.userHome.absolutePath+"/.m2/repository"
```

或

```scala
resolvers += Resolver.mavenLocal
```

通常来说，设置`resolvers`，将不会覆盖默认库地址，只是在默认库地址的基础上添加项目配置的库地址。

如果需要覆盖或者修改默认库地址，可以使用`externalResolvers`

#### 排除插件

当我们我们进行打包的时候，有时候会多个库之前重复依赖了某个文件，因为产生歧义，这时打包会失败。那么我们就需要排除一个库，或者文件。

`excludeAll`和`exclude`方法用于排除

- exclude

```scala
libraryDependencies += 
  "log4j" % "log4j" % "1.2.15" exclude("javax.jms", "jms")
```

- excludeAll

```scala
libraryDependencies +=
  "log4j" % "log4j" % "1.2.15" excludeAll(
    ExclusionRule(organization = "com.sun.jdmk"),
    ExclusionRule(organization = "com.sun.jmx"),
    ExclusionRule(organization = "javax.jms")
  )
```

`excludeAll`比`exclude`更加的灵活，但是因为前者不能使用在`pom.xml`中（Maven），所以，通常它只被用在pom.xml不需生成的场景。

我们也可以将排除规则写成如下形式：

```scala
excludeDependencies ++= Seq(
  // commons-logging is replaced by jcl-over-slf4j
  ExclusionRule("commons-logging", "commons-logging")
)
```



## 插件（Plugin）

接下来我们讲一下插件，插件的作用是添加一个sbt-site插件到编译系统。通俗来说`compile`/`project`/`target`都是插件产生的。这种属于sbt的默认插件（也叫Global plugins），默认加入这些插件。

这些插件一般可以在目录：`$HOME/.sbt/1.0/plugins/`

除此之外，还有一些第三方插件。例如：`assembly`打包插件

如何声明一个插件，我们在`例子`中已经说明了

`hello/project/assembly.sbt`

```scala
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.11.2")
```

那如何精确控制一个插件呢？

- `enablePlugins`显式定义一个插件，并使用

```scala
lazy val util = (project in file("util"))  .enablePlugins(FooPlugin, BarPlugin)  .settings(    name := "hello-util"  )
```

- `disablePlugins`显示去掉一个插件，并使用。主要用于去掉一些默认插件

```scala
lazy val util = (project in file("util"))
  .enablePlugins(FooPlugin, BarPlugin)
  .disablePlugins(plugins.IvyPlugin)
  .settings(
    name := "hello-util"
  )
```

可以通过命令行查看当前sbt使用了哪些插件：`plugins`

通常来说，我们会在`project/plugins.sbt`文件中定义我们所需要的所有插件

当然，我们也可以单独为`build.sbt`中声明的每个项目定义自己的插件，这里就不过多阐述了。