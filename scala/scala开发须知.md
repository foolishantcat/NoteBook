# Scala开发须知

[TOC]

​	scala一般用于开发高并发高可用的网络后台程序，也可以用于开发spark程序。以下先介绍如何创建一个scala后台（命令行）程序需要的步骤。

## 开发环境搭建

- IDE：intelliJ IDEA community（社区版本）
- scala安装包
- sbt安装包
- jdk使用1.8就ok

以上包自行安装需要的版本



创建sbt工程：File-->New -->Project

![new_project](./new_project.png)

新建工程后会，生成的目录结构如下：

|--.idea（工程文件）

|--project（项目文件夹）

|--src（源代码目录）

​		|--main

​			|--scala（源码包放置在该目录下）

​		|--test（单元测试目录）

​			|--scala

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

- Idea（scala）编译须知：

**scala不同大版本之间（如2.11和2.12）编译器所编译的jar包无法相互调用，会出现找不到Method的异常**

使用msi镜像安装scala，同一台机器只能安装一个版本

出错信息类似如下：

```shell
java.lang.NoSuchMethodError: scala.Predef$.ArrowAssoc(LLjava/lang/Object;
...
..
.
```

目前有四种编译/打包方式：

1. 使用PowerShell sbt命令行进行编译
2. 使用Idea Terminal 调用sbt进行编译（同1）
3. 使用Idea build编译
4. 使用 maven-scala-plugin 插件进行编译（仅java mvn推荐这种方式）

几种编译方式对比：

- 使用PowerShell sbt

调用的是windows配置的scala编译器进行编译，编译器跟随scala版本

windows本机安装的是scala 2.12.8版本，所以编译器也是2.12.8版本

- 使用Idea build

调用的是File-->Project Structure-->Global Libraries里面声明的scala编译器进行编译

该方式比较麻烦，而且如果不配置META_INF文件，会出现如下错误：

```shell
Error: Invalid or corrupt jarfile jar
```

这个报错表示找不到入口函数

推荐不要使用这种方式打包

**综上所述，使用sbt进行命令行（也可以使用Idea Terminal）打包是比较靠谱的**

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
清除target下生成的文件
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

编译中遇到的小bug：

```shell
sbt:DSP> [error] (compile:protocGenerate) error occurred while compiling protobuf files: Cannot run program "C:\Users\ethancao\protocjar5270970070978028348\bin\protoc.exe": CreateProcess error=1392, 文件或目录损坏且无法读取。

解决办法：
删除对应用户C:\Users\ethancao\protocjar5270970070978028348文件，一并删除类似protojar*文件，clean之后，重新编译即可
```

## 运行jar

有两种方式：

- 当只有一个main函数的jar包

```shell
java -jar **.jar
```

- 当有多个main函数入口的jar包，需要指明入口main函数

```shell
java -cp **.jar package.Main.ClassName > domainlog.out 2>&1 & tailf domain.out
```

其中-cp是将jar文件假如到classpath，这样java class loader就会找到匹配的类

& tailf domain.out 表示执行完前面的命令并执行tailf查看日志命令

## 命令行模式

在shell环境（windows cmd）直接运行scala进入命令行模式

```shell
$scala
切换shell环境
scala>
```

## 日志配置

我们今天要讲的一个日志组件：log4j 2.x

官方网址： http://logging.apache.org/log4j/2.x/ 

log4j能做什么？

1. 将信息送到控制台，文件，GUI组件等
2. 控制每条信息的输出格式
3. 将信息分类，定义信息级别，细致地控制日志的输出

引用方式：

```scala
libraryDependencies ++= Seq(
  "org.apache.logging.log4j" % "log4j-api-scala_2.11" % "11.0",
  "org.apache.logging.log4j" % "log4j-core" % "2.10.0",
  "org.apache.logging.log4j" % "log4j-api" % "2.10.0"
)
```

java包引用方式：

```xml
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-api-scala_${scala.binary.version}</artifactId>
	<version>11.0</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.apache.logging.log4j/log4j-core -->
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-core</artifactId>
	<version>2.10.0</version>
</dependency>
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-api</artifactId>
	<version>2.10.0</version>
</dependency>
```



在resource目录下面添加log4j2.xml文件，内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration status="error">
    <!--     先定义所有的appender -->
    <appenders>
        <!--         这个输出控制台的配置 -->
        <Console name="Console" target="SYSTEM_OUT">
            <!--             控制台只输出level及以上级别的信息（onMatch），其他的直接拒绝（onMismatch） -->
            <ThresholdFilter level="trace" onMatch="ACCEPT" onMismatch="DENY"/>
            <!--             这个都知道是输出日志的格式 -->
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class{36} %L %M - %msg%xEx%n"/>
        </Console>

        <!--         文件会打印出所有信息，这个log每次运行程序会自动清空，由append属性决定，这个也挺有用的，适合临时测试用 -->
        <!--         append为TRUE表示消息增加到指定文件中，false表示消息覆盖指定的文件内容，默认值是true -->
        <File name="log" fileName="log/test.log" append="false">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class{36} %L %M - %msg%xEx%n"/>
        </File>

        <!--          添加过滤器ThresholdFilter,可以有选择的输出某个级别以上的类别  onMatch="ACCEPT" onMismatch="DENY"意思是匹配就接受,否则直接拒绝  -->
        <File name="ERROR" fileName="logs/error.log">
            <ThresholdFilter level="error" onMatch="ACCEPT" onMismatch="DENY"/>
            <PatternLayout pattern="%d{yyyy.MM.dd 'at' HH:mm:ss z} %-5level %class{36} %L %M - %msg%xEx%n"/>
        </File>

        <!--         这个会打印出所有的信息，每次大小超过size，则这size大小的日志会自动存入按年份-月份建立的文件夹下面并进行压缩，作为存档 -->
        <RollingFile name="RollingFile" fileName="logs/web.log"
                     filePattern="logs/$${date:yyyy-MM}/web-%d{MM-dd-yyyy}-%i.log.gz">
            <PatternLayout pattern="%d{yyyy-MM-dd 'at' HH:mm:ss z} %-5level %class{36} %L %M - %msg%xEx%n"/>
            <SizeBasedTriggeringPolicy size="2MB"/>
        </RollingFile>
    </appenders>

    <!--     然后定义logger，只有定义了logger并引入的appender，appender才会生效 -->
    <loggers>
        <!--         建立一个默认的root的logger -->
        <root level="debug">
            <appender-ref ref="RollingFile"/>
            <appender-ref ref="Console"/>
            <appender-ref ref="ERROR" />
            <appender-ref ref="log"/>
        </root>

    </loggers>
</configuration>
```

- 添加HasLogger特性（trait）

```scala
// 用于给其他类继承，使得继承者具有打印日志的能力
trait HasLogger {
  implicit val log: Logger = LogManager.getLogger(this.getClass)
}
```

- 使用方式：使用的类（object和class）使用extends或者with继承该特性（trait）

> - 日志级别：
> > trace：追踪，就是程序推进一下，可以写个trace输出
> >
> > debug：调试，一般作为最低级别，trace基本不用。
> >
> > info：输出重要的信息，使用较多
> >
> > warn：警告，有些信息不是错误信息，但也要给程序员一些提示。
> >
> > error：错误信息。用的也很多。
> >
> > fatal：致命错误。级别较高，这种级别不用调试了，重写吧……

机制：如果一条日志信息的级别大于等于配置文件的级别，就记录

- 输出源：

Console（输出到控制台）、FILE（输出到文件）等。

> - 布局方式：

> > SimpleLayout：以简单的形式显示
>>
> > HTMLLayout：以HTML表格显示
>>
> > PatternLayout：自定义形式显示
>>
> > 在Log4J2中基本采用PatternLayout自定义日志布局。

>- 自定义格式
>
>>%t：线程名称
>>
>>%p: 日志级别
>>
>> %c：日志消息所在类名 
>>
>> %m：消息内容 
>>
>> %M：输出执行方法 
>>
>>%d：发生时间，%d{yyyy-MM-dd HH:mm:ss,SSS}，输出类似：2011-10-18 22:10:28,921
>>
>>%x: 输出和当前线程相关联的NDC(嵌套诊断环境),尤其用到像java servlets这样的多客户多线程的应用中。
>>
>>%L：代码中的行数
>>
>>%n：**换行**

1.引入之后在scala object 类和包中引用时看官网给的例子是extends base with logging ，后来才知道with是scala中多继承使用的关键字
也就是说使用时直接在类名或者object 名后加上extends logging就可以了。
2.然后在下面的方法中使用logger.debug("信息") 或者 error，warn等就可以了。


## 语法解析

### scala深拷贝

复写（overwrite）clone函数

### 无参方法

调用无参方法比如current时，你可以写上()，也可以不写：

```scala
myCounter.current	//ok
myCounter.current()	//ok
```

应该使用哪一种形式呢？我们认为对于“改值器方法”，即改变对象状态的方法使用()，而对于取值器方法不会改变对象状态的方法去掉()是不错的风格。
当然，你可以通过以不带()的方式声明current来强制这种风格：

```scala
class Counter {
	def current = value		//定义中不带()
}
```

这样一来类的使用者旧必须用myCounter.current，不带圆括号来调用该方法。

- “方法”和“函数”

定义一个方法：

```scala
def m(x: Int) = 2*3
```

定义一个函数：

```scala
val f = (x: Int) => 2*3
```

方法不能作为最终表达式出现：

```shell
scala> m
<console>:13: error: missing argument list for method m
Unapplied methods are only converted to functions when a function type is expected.
You can make this conversion explicit by writing `m _` or `m(_)` instead of `m`.
       m
       ^
```

函数可以作为最终表达式出现：

```shell
scala> val f = (x: Int) => 2*3
f: Int => Int = $$Lambda$1046/2062667890@3ace6346
```

而无参方法可以作为最终表达式出现，其实这属于方法“调用”，scala规定无参函数的调用可以省略括号

```shell
scala> def m1() = 1+2
m1: ()Int

scala> m1
res1: Int = 3
```

**参数列表对于方法是可选的，但是对于函数是强制的**

方法可以没有参数列表（或空）：

```shell
scala> def m2 = 100
m2: Int
scala> def m3() = 100
m3: ()Int
```

而，函数必须有参数列表，否则报错：

```shell
scala> var f1 = => 100
<console>:1: error: illegal start of simple expression
       var f1 = => 100
                ^
```

函数可以有一个空的参数列表：

```shell
scala> var f2 = () => 100
f2: () => Int = $$Lambda$1057/1141137903@5977bdea
```

**方法名意味着方法调用，函数名只是代表函数自身**

因为方法不能作为最终的表达式存在，所以如果你写了一个方法的名字并且该方法不带参数（没有参数列表或者无参）

该表达式的意思是：调用该方法得到最终的表达式（结果）

函数可以作为最终表达式出现，如果你写下函数的名字，函数调用并不会发生，该函数自身将作为最终的表达式进行返回，如果要强制调用一个函数，你**必须**在函数后面写()

```shell
scala> //该方法没有参数列表

scala> m2
res11: Int = 100

scala> //该方法有一个空的参数列表

scala> m3
res12: Int = 100

scala> //得到函数自身，不会发生函数调用

scala> f2
res13: () => Int = <function0>

scala> //调用函数

scala> f2()
res14: Int = 100
```

**为什么在函数出现的地方我们可以提供一个方法**

```shell
scala> val myList = List(3,56,1,4,72)
myList: List[Int] = List(3, 56, 1, 4, 72)

scala> // map()参数是一个函数

scala> myList.map((x) => 2*x)
res15: List[Int] = List(6, 112, 2, 8, 144)

scala> //尝试给map()函提供一个方法作为参数

scala> def m4(x:Int) = 3*x
m4: (x: Int)Int

scala> //正常执行

scala> myList.map(m4)
res17: List[Int] = List(9, 168, 3, 12, 216)
```

这是因为，如果期望出现函数的地方我们提供了一个方法的话，该方法就会自动被转换成函数。该行为被称为ETA expansion。

这样的话使用函数将会变得简单很多。你可以按照下面的代码验证该行为：

```shell
scala> //期望出现函数的地方，我们可以使用方法

scala>  val f3:(Int)=>Int = m4
f3: Int => Int = <function1>

scala> //不期望出现函数的地方，方法并不会自动转换成函数

scala> val v3 = m4
<console>:8: error: missing arguments for method m4;
follow this method with `_‘ if you want to treat it as a partially applied function
       val v3 = m4
                ^
```

 利用这种自动转换，我们可以写出很简洁的代码，如下面这样 

```shell
scala> //10.<被解释成obj.method，即整形的<的方法，所以该表达式是一个方法，会被解释成函数

scala> myList.filter(10.<)
res18: List[Int] = List(56, 72)
```

因为在scala中操作符被解释称方法

- 前缀操作符：op obj 被解释称obj.op
- 中缀操作符：obj1 op obj2被解释称obj1.op(obj2)
- 后缀操作符：obj op被解释称obj.op

你可以写成10<而不是10.<

```shell
scala> myList.filter(10<)
warning: there were 1 feature warning(s); re-run with -feature for details
res19: List[Int] = List(56, 72)
```

**如何强制把一个方法变成函数**

 可以在方法名后面加一个下划线强制变成函数，部分应用函数 

```shell
scala> val f4 = m4 _
f4: Int => Int = <function1>

scala> f4(2)
res20: Int = 6
```

**传名参数是一个方法**

 传名参数实质是一个没有参数列表的方法。正是因此你才可以使用名字调用而不用添加() 

```shell
scala> //使用两次‘x‘，意味着进行了两次方法调用

scala> def m1(x: => Int)=List(x,x)
m1: (x: => Int)List[Int]

scala> import util.Random
import util.Random

scala> val r = new Random()
r: scala.util.Random = scala.util.Random@d4c330b

scala> //因为方法被调用了两次，所以两个值不相等

scala> m1(r.nextInt)
res21: List[Int] = List(-1273601135, 2004676878)
```

 如果你在方法体部分缓存了传名参数（函数），那么你就缓存了值（因为x函数被调用了一次） 

```shell
scala> //把传名参数代表的函数缓存起来

scala> def m1(x: => Int) ={val y=x;List(y,y)}
m1: (x: => Int)List[Int]

scala> m1(r.nextInt)
res22: List[Int] = List(-1040711922, -1040711922)
```

 能否在函数体部分引用传名参数所代表的方法呢，是可以的(缓存的是传名参数所代表的方法)。 

```shell
scala> def m1(x: => Int)={val y=x _;List(y(),y())}
m1: (x: => Int)List[Int]

scala> m1(r.nextInt)
res23: List[Int] = List(-1982925840, -933815401)
```

### 参数传递

**val与def**

`def`用于定义方法，`val`定义值。对于[返回函数值的方法]与[直接使用`val`定义的函数值]之间存在微妙的差异，即使他们都定义了相同的逻辑。例如：

```scala
val max = (x: Int, y: Int) => if (x > y) x else y 
def max = (x: Int, y: Int) => if (x > y) x else y 
```

**语义差异**

虽然两者之间仅存在一字之差，但却存在本质的差异。

1.  `def`用于定义「方法」，而`val`用于定义「值」。
2.  `def`定义的方法时，方法体并未被立即求值；而`val`在定义时，其引用的对象就被立即求值了。
3.  `def`定义的方法，每次调用方法体就被求值一次；而`val`仅在定义变量时仅求值一次。

例如，每次使用`val`定义的`max`，都是使用同一个函数值；也就是说，如下语句为真。

```scala
max eq max   // true
```

而每次使用`def`定义的`max`，都将返回不同的函数值；也就是说，如下语句为假。

```scala
max eq max   // false
```

其中，`eq`通过比较对象`id`实现比较对象间的同一性的。

**lazy惰性**

`def`在定义方法时并不会产生实例，但在每次方法调用时生成不同的实例；而`val`在定义变量时便生成实例，以后每次使用`val`定义的变量时，都将得到同一个实例。

`lazy`的语义介于`def`与`val`之间。首先，`lazy val`与`val`语义类似，用于定义「值(value)」，包括函数值。

```scala
lazy val max = (x: Int, y: Int) => if (x > y) x else y 
```

其次，它又具有`def`的语义，它不会在定义`max`时就完成求值。但是，它与`def`不同，它会在第一次使用`max`时完成值的定义，对于以后再次使用`max`将返回相同的函数值。

**参数传递**

`Scala`存在两种参数传递的方式。

- Pass-by-Value：按值传递
- Pass-by-Name：按名传递

**按值传递**

默认情况下，`Scala`的参数是按照值传递的。

```ruby
def and(x: Boolean, y: Boolean) = x && y
```

对于如下调用语句：

```scala
and(false, s.contains("horance"))
```

表达式`s.contains("horance")`首先会被立即求值，然后才会传递给参数`y`；而在`and`函数体内再次使用`y`时，将不会再对`s.contains("horance")`表达式求值，直接获取最先开始被求值的结果。

**传递函数**

将上例`and`实现修改一下，让其具有函数类型的参数。

```scala
def and(x: () => Boolean, y: () => Boolean) = x() && y()
```

其中，`() => Boolean`等价于`Function0[Boolean]`，表示参数列表为空，返回值为`Boolean`的函数类型。

调用方法时，传递参数必须显式地加上`() =>`的函数头。

```scala
and(() => false, () => s.contains("horance"))
```

此时，它等价于如下实现：

```scala
and(new Function0[Boolean] { 
  def apply(): Boolean = false
}, new Function0[Boolean] {
  def apply(): Boolean = s.contains("horance")
}
```

此时，`and`方法将按照「按值传递」将`Function0`的两个对象引用分别传递给了`x`与`y`的引用变量。但时，此时它们函数体，例如`s.contains("horance")`，在参数传递之前并没有被求值；直至在`and`的方法体内，`x`与`y`调用了`apply`方法时才被求值。

也就是说，`and`方法可以等价实现为：

```scala
def and(x: () => Boolean, y: () => Boolean) = x.apply() && y.apply()
```

**按名传递**

通过`Function0[R]`的参数类型，在传递参数前实现了延迟初始化的技术。但实现中，参数传递时必须构造`() => R`的函数值，并在调用点上显式地加上`()`完成`apply`方法的调用，存在很多的语法噪声。

因此，`Scala`提供了另外一种参数传递的机制：按名传递。按名传递略去了所有`()`语法噪声。例如，函数实现中，`x`与`y`不用显式地加上`()`便可以完成调用。

```php
def and(x: => Boolean, y: => Boolean) = x && y
```

其次，调用点用户无需构造`() => R`的函数值，但它却拥有延迟初始化的功效。

```scala
and(false, s.contains("horance"))
```

**借贷模式**

资源回收是计算机工程实践中一项重要的实现模式。对于具有`GC`的程序设计语言，它仅仅实现了内存资源的自动回收，而对于诸如文件`IO`，数据库连接，`Socket`连接等资源需要程序员自行实现资源的回收。

该问题可以形式化地描述为：给定一个资源`R`，并将资源传递给用户空间，并回调算法`f: R => T`；当过程结束时资源自动释放。

> - Input: Given resource: R
> - Output：T
> - Algorithm：Call back to user namespace: f: R => T, and make sure resource be closed on done.

因此，该实现模式也常常被称为「借贷模式」，是保证资源自动回收的重要机制。本文通过`using`的抽象控制，透视`Scala`在这个领域的设计技术，以便巩固「按名传递」技术的应用。

**控制抽象：`using` **

```scala
import scala.language.reflectiveCalls

object using {
  type Closeable = { def close(): Unit }

  def apply[T <: Closeable, R](resource: => T)(f: T => R): R = {
    var source = null.asInstanceOf[T]
    try {
      source = resource
      f(source)
    } finally {
      if (source != null) source.close
    }
  }
}
```

**客户端**

例如如下程序，它读取用户根目录下的`README.md`文件，并传递给`using`，`using`会将文件句柄回调给用户空间，用户实现文件的逐行读取；当读取完成后，`using`自动关闭文件句柄，释放资源，但用户无需关心这个细节。

```scala
import scala.io.Source
import scala.util.Properties

def read: String = using(Source.fromFile(readme)) { 
  _.getLines.mkString(Properties.lineSeparator)
}
```

**鸭子编程**

`type Closeable = { def close(): Unit }`定义了一个`Closeable`的类型别名，使得`T`必须是具有`close`方法的子类型，这是`Scala`支持「鸭子编程」的一种重要技术。例如，`File`满足`T`类型的特征，它具有`close`方法。

**惰性求值**

`resource: => T`是按照`by-name`传递，在实参传递形参过程中，并未对实参进行立即求值，而将求值推延至`resource: => T`的调用点。

对于本例，`using(Source.fromFile(source))`语句中，`Source.fromFile(source)`并没有马上发生调用并传递给形参，而将求值推延至`source = resource`语句。

### 使用case class

当一个类被声明为case class时，编译器会自动进行如下操作：

1. 构造器中参数如果没有被声明为var，则默认为val类型
2. 自动创建伴生对象，同事在伴生对象中实现apply()方法，这样在使用时就不用显示地使用new对象
3. 伴生对象中同样可以实现unapply()，从而可以将case class应用于模式匹配
4. 添加天然的hashCode、equals和toString方法
5. 生成一个copy方法以支持实例a生成另一个实例b，实例b可以指定构造函数参数与a一致或不一致

### "_" 默认赋值

在java中，作为类的属性时，变量不需要立刻初始化，但是在scala中必须要立刻初始化。

1. val变量定义的时候必须复制

2. var的变量可以使用默认初始化，即用下划线（"_"）对变量赋值，但是使用的时候要注意：

   2.1 默认初始化的变量类型要明确

   ```scala
   class Person {
       var age = _	//error
   }
   
   class Person {
       var age: Int = _	//right
   }
   ```

   2.2 对于不同的类型变量，虽然都用下划线，但是初始化的值不同

   ```scala
   class Person {
       var age: Int = _	// 初始化为0
       var name: String = _	// 初始化为null
       var weight: Double = _	// 初始化为0.0，同Float
       var score: Set[Int] = _	// 初始化为null
   }
   ```

3. 可以使用代码块和三元符来做到位val类型的变量赋值

### 字符串截取

```scala
val a = "aa-bc-xx"
val i = a.indexOf("-")
val x = a.indexOf("-",i)

val one = a.substring(0,i)
print(one)    //aa

val two = a.substring(i+1,x)
print(two) //bc

val three = a.substring(x+1)
print(three)   //xx
```

### String单引号和三引号

例如下代码,如果要换行,必须在代码中添加换行符\n\r

```scala
val s1:String = "456 sldjf\n\r  slkfjl lskjfls "
```

如果换成三引号,可以在代码中直接回车

```scala
val s2:String = """456 sldjf
            lkfjl lskjfls """
```


另外如果字符串中想保留原意(例如三引号中包裹引号),也可以用三引号

```scala
val s1:String = """select * from student where name = "tom""""
```

### break和continue实现

```scala
package com.padluo.spark.scala.basic

import scala.util.control.Breaks._

object BreakTest {
  def main(args: Array[String]): Unit = {
    // break
    breakable {
      for (i <- 1 to 10) {
        if (i == 2) {
          break()
        }
        println(i)
      }
    }

    // continue
    for (i <- 1 to 10) {
      breakable {
        if (i == 2) {
          break()
        }
        println(i)
      }
    }

  }
}
```

`0 until 10`和`0 to 10`的区别，until是0到9，相当于<，to是0到10，相当于<=

## 多线程

### 并行编程

​	scala中的actor能够实现并行编程的强大功能，他是基于事件模板的并发机制。scala是运用消息的发送、接收实现多线程的。使用scala能够更容易地实现多线程应用地开发。

​	传统java并发变成与scala actor编程的区别

| Java内置线程模型                                    | Scala Actor模型                      |
| --------------------------------------------------- | ------------------------------------ |
| “共享数据-锁”模型（share data and lock）            | share nothing                        |
| 每个object有一个monitor，监视多线程对共享数据的访问 | 不共享数据，actor之间通过message通讯 |
| 加锁的代码端用synchronized标识                      |                                      |
| 死锁问题                                            |                                      |
| 每个线程内部是顺序执行的                            | 每个actor内部是顺序执行的            |

​	对于Java，我们都直达送它地多线程实现需要对共享资源（变量、对象等）使用synchronized关键字进行代码块同步、对象锁互斥等。而且，常常一大块try...catch语句块中加上wait方法、notify方法、notifyAll方法是让人很头疼地。原因就在于Java中多数使用的是可变状态地对象资源，对这些资源进行共享来实现多线程变成的话，控制好资源竞争与防止对象状态被意外修改是非常重要的，而对象状态地不可变性也是难以保证的。而在scala中，我们可以通过赋值不可变状态的资源（即对象，scala中一切都是对象，连函数、方法也是）的一个副本，再基于Actor的消息发送、接受机制进行并行编程。

### 并发编程

​	Scala中的并发编程思想与Java中的并发编程思想完全不一样，scala中的actor事一种不共享数据，依赖于消息传递的一种并发编程模式，避免了思索、资源争夺等情况。在具体实现的过程中，scala中的actor会不断的循环自己的邮箱，并通过receive偏函数进行消息的模式匹配并进行响应的处理。

​	如果actor A和actor B要相互沟通的话，首先A要给B传递一个消息，B会有一个收件箱，然后B会不断的循环自己的收件箱，若看见A发过来的消息，B就会解析A的消息并执行，处理完之后就有可能将处理的结果通过邮件的方式发送给A。

- Actor方法执行顺序

调用start()方法启动Actor

调用start()方法后其act()方法会被执行

scala Actor向Actor发送消息

- 发送消息的方式

! 发送异步消息，没有返回值

!? 发送同步消息，等待返回值

!! 发送一部消息，返回值事Future[Any]

- 同步交互与异步交互

Java中交互方式分为同步消息处理和异步消息处理两种：

同步交互：指发送一个请求，需要等待返回，然后才能够发送下一个请求，有一个等待过程；

异步交互：指发送一个请求，不需要等待返回，随时可以再发送下一个请求，即不需要等待。

### scala Actor和akka Actor

​	Actor本身来说是一个原语模型，scala本身实现了actor，但是后来者akka认为scala自身模型并不完善，Akka中的actor是生产级别的，完善的解决方案。慢慢的，在后面的版本里面scala actor将被akka actor取代。