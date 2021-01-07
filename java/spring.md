



# Java Spring日常使用详解

以下主要是基于springframework的使用心得

## Annotations

`Java annotations` 被用于提供`元数据`给Java代码。作为`元数据`，它并不直接影响java代码。但是会给java代码添加一些特殊的效果。有点类似python的装饰器的概念，区别就是python是解释性的语言，语法和使用比较，java更加规范和强大。

Java annotations从Java 5之后被添加到Java中。这表示Java8、9都是支持的。

### Java annotations 作用：

- 编译器说明（Compiler instructions）
- 编译运行时说明（Build-time instructions）
- 运行时说明（Runtime instructions）

Java annotations能够被用于Build-time，也就是编译项目的时候。编译过程包括生成源码，编译源码，生成xml文件（例如：部署脚本），打包`jar`包等。

### 反编译获取Annotations

一般来说，java annotations在java源码编译之后就会消失。但是假如你声明了一个自定义的annotations在`runtime`仍然生效的话，那么你就可以通过Java反射机制（`Java Reflection`）获取到annotations。比如我们在使用`IntelliJ idea`查看项目代码的时候，会遇到一些annotations，这时候，跳转到其定义的`代码文件`，会在上方出现：

```java
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//
```

这个就是因为使用了`runtime`配置了annotations，所以可以通过反射机制，通过java反编译器将源码编译出来。

### 编写Annotaions

可以通过像编写一个java类或者接口的方式编写一个annotations，`@interface`是修饰annotaions必要的字段。从这个修饰来看，annotations其实是一个比较特殊的`interface(接口)`。示例代码：

```java
@interface MyAnnotation {

    String   value();

    String   name();
    int      age();
    String[] newNames();

}
```

可以看到，可以定义一些成员变量，就像定义接口一样。可以使用所有的java原始类型作为annotations的元素数据类型。当然，你也可以使用一个`arrays`作为一个数据类型。但是，你不能使用一个复杂对象作为数据类型。

Annotations使用示例：

```java
@MyAnnotation(
    value="123",
    name="Jakob",
    age=37,
    newNames={"Jenkov", "Peterson"}
)
public class MyClass {


}
```

当然，也可以指定annotations中成员变量的默认值：

```java
@interface MyAnnotation {

    String   value() default "";

    String   name();
    int      age();
    String[] newNames();

}
```

当然我们也可以在使用annotations的时候指定那些没有设置默认值的成员变量，可以不为有默认值的成员变量指定默认值，例如：

```java
@MyAnnotation(
    name="Jakob",
    age=37,
    newNames={"Jenkov", "Peterson"}
)
public class MyClass {


}
```

#### @RetentionPolicy

同时还可以设置annotations的保留方式`@RetentionPolicy`，前文已经提到过了，下面是保留方式的设置方式：

```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)

@interface MyAnnotation {

    String   value() default "";

}
```

`RetentionPolicy`还包含两个可选的保留方式枚举类型，他们是：

- RetentionPolicy.CLASS，它表示annotations可以被保留到`.class`文件中。但是并不可以在java虚拟机运行时被访问。这是annotations的默认保留方式。
- RetentionPolicy.SOURCE，表示annotations仅被保留在原代码中。这种模式一般被用于，当你需要使用编译工具配合annotations对代码进行浏览/扫描的时，并不希望`.class`文件被annotations进行不必要的污染。

#### @Target

指定annotations的使用目标范围，指定`@Target`即可，例如：

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Target;

@Target({ElementType.METHOD})
public @interface MyAnnotation {

    String   value();
}
```

可以看到该annotations的使用范围被指定为方法（`METHOD`），除此之外，还可以使用；

- ElementType.ANNOTATION_TYPE
- ElementType.CONSTRUCTOR
- ElementType.FIELD
- ElementType.LOCAL_VARIABLE
- ElementType.METHOD
- ElementType.PACKAGE
- ElementType.PARAMETER
- ElementType.TYPE

以上大部分枚举值可以通过字面意思理解，当然还有两个是不行的。

`ANNOTATION_TYPE`表示仅可以被用于另外一个annotations，就像`@Target`和`Retention`这样子。这可能是由于annotations没有`继承`这个概念，所以用这个使用范围去代替了`继承`。

`TYPE`表示可以适用于所有的类型，典型的类型：`class`、`interface`、`annotation`

#### @Inherited

该装饰器表示被该装饰器所装饰的类`class`必须被一个子类所继承。例子：

```java
java.lang.annotation.Inherited

@Inherited
public @interface MyAnnotation {

}
```

```java
@MyAnnotation
public class MySuperClass { ... }
```

```java
public class MySubClass extends MySuperClass { ... }
```

如示例代码所示，如若`MySuperClass`没有被`MySubClass`继承的话，那么在编译阶段就会报错。

#### @Documented

该装饰器比较少用，它会告诉`JavaDoc`工具，使用了该装饰器的类必须要在JavaDoc里面显示出现该annotations的描述。因为很少使用，这里就不给出使用模版了。

## @Aysnc

`org.springframework.scheduling.annotation`

springboot异步操作可以使用`@EnableAsync`和`@Async`两个注解，本质就是`多线程`和`动态代理`。

装饰器定义：

```java
@Target(value={TYPE,METHOD})
@Retention
@Documented
public @interface Aysnc
```

用于标记一个方法可以异步执行，也可以被用于类型级别，被这个类型锁标记的方法可以异步执行。注意，`@Async`不可以在已经被声明了`@Configuration`的类里面被使用。例如：

```java
@Configuration
public class Test{
  @Async
  public void TestMethod() {	/* 这样是不合法的 */
    ...
  }
}
```

被修饰的方法返回值只可能是`void`或`Feture`类型（**否则异步失效**）。一般来说说，会声明`ListenableFuture`或`CompletableFuture`类型，这两种类型具有更为丰富的异步任务交互体验。

当返回一个`Feture`句柄时，能够被用于追踪异步方法执行的结果。

如果在Spring里面使用Aysnc装饰器，需要在启动类加上`@EnableAsync`注释。

此外，`@Async`注释用在非`public`方法上面，异步会失效

当spring框架里面，使用`@Async`时，被`@Async`修饰的`public`方法，只能被`Controller`直接调用时才会生效。

此外，被修饰的函数，调用者必须是外部使用者，如果内部函数调用会出现代理绕过的问题，从而无法执行异步，不会出错，会变成同步操作，看起来就是`@Async`失效的状态。

## @RestController

`org.springframework.web.bind.annotation`

定义：

```java
@Target(value=TYPE)
@Retention(value=RUNTIME)
@Documented
@Controller
@ResponseBody
public @interface RestController
```

一般来说，该装饰器默认会和`@RequestMapping`和`@ResponseBody`一起使用。

`@RequestMapping("/url_path")`被用来定义http访问的路径。他们组成了Java MVC架构的基础。

## @PostMapping

定义：

```java
@Target(value=METHOD)
@Retention(value=RUNTIME)
@Documented
@RequestMapping(method=POST)
public @interface PostMapping
```

用于指定一个`HTTP POST`请求的处理方法，所以是用来修饰方法的。

特别说一下，`@PostMapping`是一种缩写方式，你也可以写成`@RequestMapping(method = RequestMethod.POST)`。

类似的还有：

```java
@GetMapping
@PutMapping
@DeleteMapping
@PatchMapping
@RequestMapping
```

## @RequestBody

`org.springframework.web.bind.annotation`

定义：

```java
@Target(value=PARAMETER)
@Retention(value=RUNTIME)
@Documented
public @interface RequestBody
```

该装饰器表明在web请求输入时，方法参数将被绑定为web请求的一部分（http请求参数）。通过`HttpMessageConverter`决定方法参数时如何转化成http请求body参数。你也可以添加`@Valid`装饰器去自动检查参数是否有效。

## @RequestHeader

`org.springframework.web.bind.annotation`

定义：

```java
@Target(value=PARAMETER)
@Retention(value=RUNTIME)
@Documented
public @interface RequestHeader
```

声明该参数被绑定到http请求的请求头。

一般来说，这个参数的类型可以是`Map<String, String>`或者`HttpHeaders`。

## @Validated

`org.springframework.validation.annotation`

主要用于参数验证，可以配合用于检查类、方法、参数等是否有效。

比如：

```java
@Validated
public class Test{
  @NotNull
  @Size(max=32, message="code is null")
  private String code;
}
```

假如无效，会统一抛出异常。

## @RequestParam

`org.springframework.web.bind.annotation`

定义：

```java
@Target(value=PARAMETER)
@Retention(value=RUNTIME)
@Documented
public @interface RequestParam
```

表明被修饰的参数将被当成web请求参数对待。

## @Data

`lombok`

使用这个注解，就不用再去手写Getter，Setter，equals，canEqual，hasCode，toString等方法了，注解后在编译时会自动加进去。

## @AllArgsConstructor

`lombok`

使用后添加一个构造函数，该构造函数含有所有已声明字段属性参数。

## @NoArgsConstructor

`lombok`

使用后创建一个无参数构造函数

## @Builder

`lombok`

关于Builder较为复杂一些，Builder的作用之一是为了解决在某个类有很多构造函数的情况下，也省去写很多构造函数的麻烦，在设计模式思想是：**用一个内部类去实例化一个对象，避免一个类出现过多构造函数**。

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class test1{
  String name;
  String age;
  String sex;
}
```

```java
public static void main(String[] args) {
  test1 t1 = new test1.test1Builder()
    .name("wang")
    .age("12")
    .sex("man")
    .build();
}
```

可以看出，可以使用`Builder`替代原本可能要写很多个构造函数，相当于临时自定义构造函数。

## @RestControllerAdvice

`org.springframework.web.bind.annotation`

定义：

```java
@Target(value=TYPE)
@Retention(value=RUNTIME)
@Documented
@ControllerAdvice
@ResponseBody
public @interface RestControllerAdvice
```

被声明了该装饰器的类型，作为一个`@ExceptionHandler`的控制器，用于处理`Controller`所产生的异常消息。

```java
@RestControllerAdvice
public class ApplicationExceptionHandler {
    @ExceptionHandler(MissingServletRequestParameterException.class)
    protected Response handleMissingServletRequestParameterException(
            MissingServletRequestParameterException e) {
        log.info(e.getMessage());
        return new Response(Code.PARAM_INVALID,
                e.getParameterName() + " parameter is missing");
    }
}
```

可以看到异常处理完成之后，返回的类型依然是`Response`，跟正常返回类型保持一致，接口调用者可以正常接收到异常消息。

## @SpringBootApplication

`org.springframework.boot.autoconfigure`

SpringBoot目前是和SpringFrameWork独立的包。所以需要独立引用。

定义：

```java
@Target(value=TYPE)
@Retention(value=RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(
  excludeFilters={
    @ComponentScan.Filter(
      type=CUSTOM, 
      classes=TypeExcludeFilter.class
    ),
  }
)
public @interface SpringBootApplication
```

声明一个`configuration`类，声明一个或者多个`@Bean`方法，并且会带有触发器`auto-configuration`和`component scanning`。

## @EnableAsync

`org.springframework.scheduling.annotation`

开启Spring的异步方法执行能力。

如果和装饰器`Configuration`所装饰的类一起使用，那么表示在整个Spring应用期间都支持异步方法执行功能。

## @Bean

`org.springframework.context.annotation`

定义：

```java
@Target(value={METHOD,ANNOTATION_TYPE})
@Retention(value=RUNTIME)
@Documented
public @interface Bean
```

表示被修饰方法产生一个`bean`，并且这个`bean`被`Spring container`所管理。通俗来说，是一个配置项。

在Spring 3.0之前的Spring核心框架中，我们启动一个Spring容器必须要使用一个`xml`文件。而到了3.x之后的版本，Spring新增了一个入口类：**AnnotationConfigApplicationContext**

简单来说，有了它之后，不用再使用xml文件进行类注入了。而是向容器中添加`Bean`所修饰的指定类即可。



## @Component

在类上使用`@Component`，使用注解，相当于下面一句xml语句：

```xml
<bean id="xxx" class="com.path.to.xxxImpl" />
```



## @Configuration

有些网上的说法说的非常复杂，其实简单理解，就是把xml注入Bean的方式，改为了注解注入的方式:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 在类中使用@Configuration，相当于添加了一个beans，是一系列bean的集合 -->
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                           http://www.springframework.org/schema/beans/spring-beans.xsd
                           http://www.springframework.org/schema/context
                           http://www.springframework.org/schema/beans/spring-context.xsd">
 
 
 
    <!--在类中使用@Component，使用注解，相当于下面一行语句-->
    <!--<bean id="useService" class="com.gyf.service.UserServiceImpl"/>-->
 
 
    <context:annotation-config/>
 
    <!--这个包下的文件都会被检测-->
    <context:component-scan base-package="com.gyf"/>
</beans>
```

@Configuration类允许通过同一个类中的其他@Bean方法来定义bean之间的依赖关系。

使用@Configuration注解，在调用类内方法的时候，需要获取参数实例的时候，会去spring的单例bean工厂中获取参数单例bean实例。

不使用@Configuration注解，实例化类内参数的时候，每次都会创建一个新的对象。



## @Bean和@Conponent的区别

要想理解这两个的区别，首先我们需要理解spring是如何管理Bean的。

spring帮助我们管理Bean分为两个部分：一个是`注册Bean`，一个是`装配Bean`。

完成这两个动作**有三种方式：自动装配、JavaConfig、XML配置**。

- 自动装配方式

使用`@Component`去告诉spring，我是一个Bean，你要来管理我，然后使用`@Autowired`注解去装配Bean（**所谓装配，就是管理对象直接的协作关系**）。

- JavaConfig方式

然后在JavaConfig中，`@Configuration`其实就是告诉spring，spring容器要怎么配置（**怎么去注册bean，怎么去处理bean之间的关系--装配**）。那么，就很好理解了。@Bean的意思就是，我要获取这个bean的时候，spring要按照这种方式去帮我获取到这个bean。

- XML方式

到了使用xml的方式，也是如此。君不见**<bean>**标签就是告诉spring怎么获取这个bean，各种<ref>就是手动的配置bean之间的关系。

用`@Bean`注解的**`方法`**：会实例化、配置并初始化一个新的对象，这个对象会由spring IoC容器管理。

```java
@Configuration
public class AppConfig {
  @Bean
  public MyService myService() {
    return new MyServiceImpl();
  }
}
```

相当于在XML文件中配置

```xml
<beans>
	<bean id="myService" class="com.xx.xx.xxImpl" />
</beans>
```

生成对象的名字：默认情况下用@Bean注解的方法名作为对象的名字。但是可以用name属性定义对象的名字。

```java
@Configuration
public class AppConfig {
  @Bean(name = "myFoo")
  public MyService myService() {
    return new MyServiceImpl();
  }
}
```

**需要注意的是：在@Component注解的类中不能定义 类内依赖的@Bean注解的方法，简单说@Component注解的类里面不能用@Bean注解方法。**

**而@Configuration是可以的**

这个也很好理解，@Component本身已经就是声明Bean的一种方式，不能嵌套使用@Bean注解。

简单总结一下：

1. @Conponent作用就相当于XML配置中的`<bean>`标签，声明了一个bean
2. @Bean需要在配置类中使用，即类上需要加上@Configuration注解
3. 两者都可以通过@Autowired装配
4. @Bean注解比@Component注解的自定义性更强，而且很多地方只能通过@Bean注解来注册bean。**比如当引用第三方库类需要装配到spring容器的时候，就只能通过@Bean注解来实现。因为无法在第三方库的源代码上加上@Component注解。**



## @Lazy

一般情况下，spring容器在启动时会创建所有的Bean对象，使用`@Lazy`注解可以将Bean对象的创建延迟到第一次使用Bean的时候。



## @Autowired

### @Autowired和@Resource

1. @Autowired和@Resource都可以用来装配Bean，都可以写在字段、setter上
2. @Autowired默认按类型装配（属于spring提供的），默认情况下必须要求依赖对象必须存在，如果要允许null值，可以设置它的required属性为false
3. @Resource是JDK1.6支持的注解，默认按照名称进行装配，名称通过name属性进行指定，如果没有指定name属性，当注解写在字段上时，默认取字段名，按照名称查找，如果注解写在setter方法上默认取属性名进行装配。

### @Autowired和@Service

传统的Spring做法是使用`.xml`文件来对bean进行注解或者是配置aop、事务，这么做有两个缺点：

1. xml文件越来越多，越来越大
2. 在java和xml之间不断来回切换，编码连贯性降低

为了解决这两个问题，spring引入注解，通过“@XXX”的方式，让注解与Java Bean紧密结合，既大大减少了配置文件的体积，又增加了Java Bean的可读性与内聚性。

@Autowired注解的意思就是，当Spring发现@Autowired注解时，将自动在代码上下文中找到和其匹配（默认是类型匹配）的Bean，并自动注入到相应的地方去。

@Autowired不仅可以修饰需要注入的属性对象，还可以修饰注入`接口`（interface）

**@Service的主要作用：**

1. 声明**.java是一个bean（如果修饰类），其他类可以直接使用@Autowired将类当做一个成员变量自动注入

```java
@Service
@Scope("prototype")
public class Zoo {
  @Autowired
  private Monkey monkey;
  @Autowired
  private Tiger tiger;
  
  public String toString() {
    return "MonkeyName:" + monkey + "\nTigerName:" + tiger;
  }
};
```

2. `@Scope`注解，因为Spring默认生产出来的bean是单例的，假如我不想单例使用怎么办，xml文件里面可以在bean里面配置scope属性。注解也是一样，配置@Scope即可，默认是“singleton”即单例，“prototype”表示原型即每次都会new一个新的出来。

## @Qualifier

使用`@Autowired`注解时spring依赖注入的绝好方法。但是有些场景下仅仅靠这个注解不足以让spring知道到底要注入哪个bean。默认情况下，@Autowired按类型装配spring bean。

如果容器中有多个相同类型的bean，则框架将抛出`NoUniqueBeanDefinitionException`，以提示有多个满足条件的bean进行自动装配。程序无法正确作出判断使用哪一个。下面有个例子：

```java
@Component("fooFormatter")
public class FooFormatter implements Formatter {
  public String format() {
    return "foo";
  }
}

@Component("barFormatter")
public class BarFormatter implements Formatter {
  public String format() {
    return "bar";
  }
}

@Component
public class FooService {
  @Autowired
  private Formatter formatter;

  //todo 
}
```

如果我们尝试将FooService加载到我们的上下文中，spring框架将抛出`NoUniqueBeanDefinitionException`。这是因为spring不知道要注入哪个bean。为了避免这个问题，有几种解决方案。我这里只讲`@Qualifier`

通过使用`@Qualifier`注解，我们可以消除需要注入哪个bean的问题。让我们重新回顾一下前面的例子，看看我们如何通过包含@Qualifier注释来支出我们想要使用哪个bean来解决问题。

```java
@Component
public class FooService {
  @Autowired
  @Qualifier("fooFormatter")
  private Formatter formatter;

  //todo 
}
```

通过将@Qualifier注解与我们想要使用的特定spring bean的名称一起进行装配，spring框架就能从多个相同类型并满足装配要求的bean中找到我们想要的，避免让spring脑裂。我们需要做的是@Component或者@Bean注解中生命的value属性以确定名称。

其实我们也可以在Fomatter实现类上使用@Qualifier注解，而不是在@Component或者@Bean中指定名称，也能达到相同的效果：

```java
@Component
@Qualifier("fooFormatter")
public class FooFormatter implements Formatter {
  public String format() {
    return "foo";
  }
}

@Component
@Qualifier("barFormatter")
public class BarFormatter implements Formatter {
  public String format() {
    return "bar";
  }
}
```

除此之外，还有另外一个注解也实现类似功能**`@Primary`**，我们也可以用来发生依赖注入的歧义时决定要注入哪个Bean。当存在多个相同的bean时，此注解定义了首选项。除非另有说明，否则将使用与@Primary注释关联的bean。

我们来看一个例子：

```java
@Bean
public Employee tomEmployee() {
  return new Employee("Tom");
}

@Bean
@Primary
public Employee johnEmployee() {
  return new Employee("john");
}
```

以上两个方法都返回相同的Employee类型。spring将注入的bean是方法johnEmployee返回的bean。这是因为它包含@Primary注解。当我们想要指定默认情况下应该注入特定类型的bean时，此注解很有用。

如果我们在某个注入点需要另一个bean，我们需要专门指出它。我们可以通过@Qualifier注解来做到这一点。例如，我们可以通过使用@Qualifier注释指定我们想要使用tomEmployee方法返回的bean。

值得注意的是，如果@Qualifier和@Primary注释都存在，那么@Qualifier注释将具有优先权。基本上，@Primary是定义了默认值，而@Qualifier则非常具体。

当然@Component也可以使用@Primary注解：

```java
@Component
@Primary
public class FooFormatter implements Formatter {
  public String format() {
    return "foo";
  }
}

@Component
public class BarFormatter implements Formatter {
  public String format() {
    return "bar";
  }
}
```

在这种情况下，@Primary注解指定了默认注入的是FooFormatter，消除了场景中的注入歧义。

## @Required

@Required注释为为了保证所对应的属性必须被设置，**@Required** 注释应用于 bean 属性的 setter 方法，它表明受影响的 bean 属性在配置时必须放在 XML 配置文件中，否则容器就会抛出一个 BeanInitializationException 异常。下面显示的是一个使用 @Required 注释的示例。*直接的理解就是，如果你在某个java类的某个set方法上使用了该注释，那么该set方法对应的属性在xml配置文件中必须被设置，否则就会报错！！！*

## @Entity

Hibernate框架（Spring ORM框架）的注解，必须与`@Id`注解结合使用

### @Table

声明此对象映射到数据库的表，通过它可以为实体指定表（table），目录（catalog）和schema的名字。该注释不是必须的，如果没有则系统使用默认值（实体的短类名）

### @Version

该注释可用于在实体Bean中添加乐观锁支持

### @Id

声明此属性为主键。该属性值可以通过应该自身创建，但是Hibernate推荐通过Hibernate生成

### @GeneratedValue

指定主键的生成策略。有如下四个值：

- TABLE：使用表保存id值，通过表产生主键
- IDENTIRY：identity column采用数据库ID自增长的方式来自增主键字段
- SEQUENCR：sequence序列产生主键
- AUTO：根据数据库的不同使用上面三个

### @Column

声明该属性与数据库字段的映射关系，例如：

```java
@Column(name="category_name" length=20)
public void getCategoryName() {
  return this.categoryName;
}
```

## @PostConstruct

使用@PostConstruct，在方法上添加@PostConstruct注解，一定要放在能被扫描到的地方（例如：`@Service`或者`@Component`注解修饰的类），如果你写在一个无法被扫描到的位置是不能执行的。

这个注解的主要作用是，在依赖被注入到`容器`之内后，会第一时间调用被PostConstruct修饰的函数，当然，这个函数，必须是`public`的，难道是外部需要通过instance实例对象来调这个函数？

## @Sheduled

这个函数用来，设定异步执行某个定时器任务。该注解通常需要spring在启动类添加修饰：`@EnableScheduling`。

需要注意的是，该注解启动的定时任务是单线程的，所以，可能会发生线程阻塞。如果需要避免线程阻塞，要配合**`implements SchedulingConfigurer`**使用。

```java
@Configuration
@Enable
class ScheduleConfig implements ShedulingConfigurer {
  @Override
  public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
    taskRegistrar.setScheduler(Executors.newScheduledThreadPool(5));
  }
}
```

以上代码，放在`@Shcheduled`修饰方法的同级类，可以启动多线程处理定时器任务。



## @Qualifier

使用`@Autowired`注解是Spring依赖注入的绝好方法。但是有些场景下仅仅靠这个注解不足以让Spring知道到底要注入哪个bean。

默认情况下，@Autowired按类型装配Spring Bean。

如果容器中有多个相同类型bean，则框架将抛出`NoUniqueBeanDefinitionException`，以提示有多个满足条件的bean进行自动装配。程序无法正确作出判断使用哪一个。

比较常见的场景就是`@Autowired`注解在了一个被多个子类实现的父类上面。

为了避免这样的问题，有几种解决方案，`@Qualifier`注解就是其中之一。

在实现类和声明类的地方，都使用Qualifier进行注解，并且使用相对应的指定名称即可。

`@Qualifier`和`@Primary`做对比：

存在相同类型的bean时，后者定义了一个首选项。除非有说明，否则将使用与`@Primary`注释关联的bean。

还有一个我们值得注意，但是不建议使用的特性:

在使用`@Autowired`进行自动装配时，如果Spring没有其他提示，将会按照需要注入的变量名称来寻找合适的bean。也可以解决依赖注入歧义的问题。（但是我感觉这个简直就是扯淡，建议大家看看就好，魔幻操作）



## @Transactional

使用spring框架的事务，真的要了解的东西太多。这里我先给个简要的结论：

- 基于TransactionDefinition、PlatformTransactionManager、TransactionStatus编程式事务管理是Spring提供的最原始的方式，通常我么不会这么写，但是了解这种方式对理解Spring事务管理的本质有很大作用
- 基于TransactionTemplate的编程式事务管理是对上一种方式的封装，使得编码更简单、清晰。
- 基于TransactionInterceptor的声明式事务是Spring声明式事务的基础，通常不建议使用这种方式，但是与前面一样对理解Spring声明式事务有很大作用。
- 基于TransactionInterceptor的声明式事务是Spring声明式事务的基础，通常也不建议使用这种方式，但是与前面一样，了解这种方式对理解Spring声明式事务有很大作用。
- 基于TransactionProxyFactoryBean的声明式事务是上种方式的改进版本，简化的配置文件的书写，这是Spring早期推荐的声明式事务管理方式，但是在Spring2.0中已经不推荐了。
- 基于<tx>和<aop>命名空间的声明式事务管理是目前推荐的方式，其最大特点是与Spring`AOP`结合紧密，可以充分利用切入表达式的强大支持，使得管理事务更加灵活。
- 基于`@Transactional`的方式将声明式事务管理简化到了极致。开发人员只需在配置文件中加上银行启用相关后处理Bean的配置，然后在需要实施事务管理的方法或者类上使用`@Transactional`指定事务规则即可实现事务管理，而且功能也不比其他方式逊色。

那么，由此可见，事务分为两种：`编程式事务`、`声明式事务`

Spring事务跨越了一个比较清晰的发展阶段，总体来说就是越来越方便了。简而言之，可以使用刀耕火种的编程式，也可以使用鸟枪换炮的声明式事务。

为了忠于人的本能--懒惰，当然首推`声明式事务`。那么下面主要介绍在使用声明式事务的过程中遇到的坑。

一般情况，我们在处理具体的业务都是在`Service`层来进行处理操作，此时如果再Service类上添加`@Transactional`注解的话，那么Service层的每一个业务方法调用的时候都会打开一个事务。

注意点：Spring默认情况下会对（RuntimeException）及其子类来进行回滚，在遇见Exception及其子类的时候则不会进行回滚操作。



## @ImportResource

`@ImportResource`和我们之前介绍的`@Value`功能很类似，都是用来进行资源文件读取。重点介绍一下`@ImportResource`。

我们先来看一个Bean的配置文件

```xml
<beans>
    <context:annotation-config/>
    <context:property-placeholder location="classpath:/com/acme/jdbc.properties"/>

    <bean class="com.acme.AppConfig"/>

    <bean class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
</beans>
```

这个使用`property-placeholder`，在使用它的时候，它会对应一个资源文件，对应一个localtion，location对应一个资源文件的存放位置。

<font color=red>`<context:property-placeholder location="classpath:/com.acme/jdbc.properties">`</font>，这句话的作用是加载properties资源文件。properties文件是一种key、value的形式的文件（**其实这种说法也不对，key-value形式文件形式有很多，这里应该是可以加载xml形式的配置文件**）。

加载了这个文件之后，在当前的文件中，可以通过`${}`的方式，`{}`里边是properties文件中的key，通过这种方式来引用properties文件中的内容。比如说常用的数据库的配置方式。

我们的配置信息通常会写在资源文件中，然后通过properties-placeholder这种方式去把它加载进来。然后在当前的配置文件中去引用它。比如说这里指定了一种数据源资源`DriverManagerDataSource`，然后可以指定这种数据源的url、username和password，它们的来源就是这个资源文件。

以上是使用xml文件配置的方式，那么如果使用注解要怎么做？（众所周知，一般spring都会支持xml的特征可注解化，这个很好理解，注解是可以被编译期间进行检查的，更加符合编译语言的天性）。

```java
@Configuration
@ImportResource("classpath:/com/acme/properties-config.xml")
public class AppConfig{

    @Value("${jdbc.url}")
    private String url;

    @Value("${jdbc.username}")
    private String username;

    @Value("${jdbc.password}")
    private String password;

    @Bean
    public DataSource dataSource() {
        return new DriverManagerDataSource(url,username,password);
    }
}
```

使用`@Configuration`，把这个类作为一个配置来使用。`@ImportResource`就是引入一个这种资源，然后资源对应一个xml文件，和前个例子差不多，xml文件也会对应一个property-placeholder。

用`@Value`这个注解从资源文件中取出它的key赋值给成员变量，包括username、password等。然后再使用@Bean这个注解去创建DriverManagerDataSource的一个对象，也就是和第一种的方式一样，去创建这个Bean对象，同时把url、username、password传入DriverManagerDataSource的构造器。

这样就达到了从资源文件中去加载资源文件的配置，并应用到Bean的创建中。

然后再配合一个带参数的类构造函数：

```java
@Bean
public class MyDriverManager {

    public MyDriverManager(String url, String userName, String password) {
        System.out.println("url : " + url);
        System.out.println("userName: " + userName);
        System.out.println("password: " + password);
    }
}
```

将从资源文件中获取的参数，注入类的构造参数中。

在使用的时候，使用@Autowired获取类的实例的时候，就会自动根据xml文件配置的参数，生成类的对象。

大体就是这样子。



## @Order

@Order注解的主要作用就是控制Bean生成的顺序，比方说@Order(1)比@Order(2)会先被初始化，这个主要用在spring启动的时候，控制一些Bean的依赖关系，了解到这么多就可以了。







## synchronized

Java中的synchronized关键字可以在多线程环境下用来作为线程安全的同步锁。本文主要对synchronized的作用，以及其有效范围进行讨论。

Java中的对象锁和类锁：java的对象所和类锁在锁的概念上基本上和内置锁是一致的，但是两个锁实际是有很大的区别的，对象锁是用于对象实例方法，或者一个对象实例上的，类锁是用于类的静态方法或者一个类的class对象上的。我们知道，类的对象实例可以有很多个，但是每个类只有一个class对象，所以不同对象实例的对象锁是互不干扰的，但是每个类只有一个类锁。但是有一点必须注意的是，其实类锁只是一个概念上的东西，并不是真实存在的。它这只是用来帮助我们理解锁定实例方法和静态方法的区别的。

synchronized关键字主要有一下几种用法：

- 非静态方法的同步
- 静态方法的同步
- 代码块





## corsConfigurer（跨域访问）

SpringBoot添加支持CORS（Cross-Origin Resource Sharing）跨域访问。它允许浏览器向跨域服务器发送Ajax请求，发破了Ajax只能访问本站内的资源限制，CORS在很多地方都有被使用，微信支付的JS支付就是通过JS向微信服务器发送跨域请求。开放Ajax访问可被跨域访问的服务器大大减少了后台开发的工作，前后台工作也可以得到很好的明确以及分工。下面是SpringBoot添加cors支持的代码：

```java
@Bean
public WebMvcConfigurer corsConfigurer() {
  return new WebMvcConfigurer() {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
      registry.addMapping("/**").allowedOrigins("*")
        .allowCredentials(true);
    }
  };
}
```

本质上是向配置xml里面添加了一行配置而已。其实这里主要是重写WebMvcConfigurationAdapter类的`addCorsMappings`方法而已。配置介绍如下：

- addMapping：配置可以呗跨域的路径，可以任意配置，可以具体到直接请求路径。
- allowedMethods：允许所有的请求方法访问该跨域资源服务器，如：**POST、GET、PUT、DELETE等**。
- allowedOrigins：允许所有的请求域名访问我们的跨域资源，可以固定单条或者多条内容，如：“http://www.baidu.com”，只有百度可以访问我们的跨域资源。
- allowedHeaders：允许所有的请求header访问，可以自定义设置任意请求头信息，如：“X-YAUTH-TOKEN”



# Java日常使用

## Runnable

`java.lang`

`@FunctionalInterface`

`public interface Runnable`

继承了`Runnable`接口的类，必须含有一个无参`run`函数，该类的实例对象会按照一个线程单独被执行。

## ExecutorService

`java.util.concurrent`

`public interface ExecutorService extends Executor`

`Executor`提供一个方法管理界面，并且观察一个用于追踪异步任务的`Future`对象。

`ExecutorService`当注入了一个新的任务之后，可以被`shut down`。

有两种关闭的方法：

1. `shutdown()`方法允许在提交的任务运行结束之前提前执行，但是不影响提交任务的执行。
2. `shutdownNow`将会禁止等待执行的任务开始，并尝试终止正在执行的任务。

任务执行方法：

1. 执行`Executor.execute(Runnable)`并返回一个`Future`用于任务取消、等待执行完毕。

## java static import

java静态引用。主要目的：将原本需要使用import导入的类所包含的静态方法的使用方式`ClassName.method()`改成不需要使用类名访问`method()`。

这样做，并没有什么太大的好处，并且不同类存在同名静态函数，会产生编译错误。

所以官方建议，除非特别说明，不建议这么使用。

## stampedLock

邮戳锁。

- 特点：

获取锁的方法，都返回一个邮戳（stamp），stamp为0表示获取失败，其余都表示成功。

释放锁的方法，都需要一个邮戳（stamp），这个stamp必须与获取锁的stamp一致。

stampedlock是不可重入的；如果一个线程已经持有了写锁，再去获取写锁的话就会造成死锁。

支持锁升级跟锁降级

使用有限次自旋，增加锁获得的几率，避免上下文切换带来的开销

乐观读不阻塞写操作，悲观读，阻塞写的操作

- 优点

相比于reentrantReadWriteLock，吞吐量大幅提升

- 缺点

api相对复杂，容易用错

内部实现相比于reetrantReadWriteLock复杂得多

- 原理

每次获取锁的时候，都会返回一个邮戳，相当于mysql里的version字段。

释放锁的时候，再根据之前的获得的邮戳，去进行锁释放

- 注意点

如果使用乐观读，一定要判断返回的邮戳是否是一开始获得到的，如果不是，要去获取悲观读锁。



## 接口实例化

按照正常来说，java的接口是不能够直接实例化的，因为接口的方法是抽象方法，没有被实现。

但是java允许直接“匿名实例化”接口类，其实本质上就是实现了接口，但是没有给这个接口命名。

```java
public interface Test1 {
  public void test1();
}

public class ImplClassTest1 {
  public implClassTest1() {
    useUnnameInterfaceImpl(new Test1{
      @Override
      public void test1(){
        System.out.println("test1 do something...");
      }
    };
  }
  
  private void useUnnameInterfaceImpl(Test1 test1);
}
```

## PO、BO、VO、POJO和DTO

- PO：persistent object 持久对象
- POJO：Plain ordinary java object 无规则简单java对象
- BO：business object 业务对象
- VO：value object 值对象/view object 表现层对象
- DTO（TO）：data transfer object 数据传输对象
- DAO：data Access object 数据访问对象



## 动态定时任务&静态定时任务

- 主要区别

动态和静态定时任务的区别就是**`执行任务周期的cron表达式是配置在文件中还是代码中`**

我认为上面的理解是不到位的，java的配置文件假如修改，也是需要发版本的，也不能算真的“动态”，

如果，能够通过接口创建定时任务，并且可以通过接口参数控制定时器的生成和销毁，那么就可以称为“动态定时任务”。

- 定时任务有三种实现

1. jdk自带的定时任务
2. Quartz插件实现的定时任务，需要引入额外的包
3. Spring Task定时调度，是对jdk的再一次封装，不用引入其他包了，用spring的包就自带

**静态、动态定时任务，只是使用场景不同，没有好坏之分**

- cron表达式

从左到右（用空格隔开）：秒 分 小时 月份中的日期 月份 星期中的日期 年份

```
每隔5秒执行一次：*/5 * * * * ?
每隔1分钟执行一次：0 */1 * * * ?
每天23点执行一次：0 0 23 * * ?
每天凌晨1点执行一次：0 0 1 * * ?
每月1号凌晨1点执行一次：0 0 1 1 * ?
每月最后一天23点执行一次：0 0 23 L * ?
每周星期天凌晨1点实行一次：0 0 1 ? * L
在26分、29分、33分执行一次：0 26,29,33 * * * ?
每天的0点、13点、18点、21点都执行一次：0 0 0,13,18,21 * * ?
```



## Java异常分类

发现错误的理想时机是编译期。然后，编译器并不能发现所有的错误，余下的问题就需要在程序运行时解决。

Java异常的明显好处，就是：降低错误处理代码的复杂度。非常像C语言的goto，但是比那个好用多了，不用考虑破坏堆栈的问题。

Java中，异常被当做对象处理，这也符合面向对象语言，一切皆为对象的理念，其基类是Throwable。

Java从Throwable直接派生出`Exception`和`Error`。其中`Exception`是可以抛出的基本类型，在Java类库、方法以及运行时故障中都可能抛出Exception异常。Exception表示`可以恢复的异常`，是编译器可以捕捉到的；`Error`表示编译时和系统错误，表示系统在运行期间出现了严重的错误，属于`不可恢复的错误`，由于这属于JVM层次的严重错误，因此这种错误会导致程序终止执行。

此外，`Exception`又分为`检查异常`和`运行时异常（RuntimeException）`。

典型的RuntimeException包括：`NullPointerException`,`ClasCastException（类型转换异常）`，`IndexOutOfBoundsException(越界异常)`，`IllegalArgumentException(非法参数异常)`，`ArrayStoreException(数组存储异常)`，`AruthmeticException(算术异常)`，`BufferOverflowException(缓冲区溢出异常)`等；

非`RuntimeException`，称为`检查异常`，包括：`IOException`,`SQLException`,`InterruptedException(中断异常-调用线程睡眠异常)`，`NumberFormatException(数字格式化异常)`等。

而按照`编译器检查方式`划分，异常又可以分为：检查型异常（`CheckedException`）和非检查型异常（`UncheckedException`）。`Error`和`RuntimeException`合起来称为`UncheckedException`，之所以这么称呼，是因为编译器不检查方法是否处理或者抛出这两种类型的异常，因此编译期间这种类型的异常也不会报错，默认由虚拟机提供处理方式。除了Error和RuntimeException这两种类型的异常外，其他异常都称为Checked异常。

在异常的处理环节，有一个点需要注意：**异常链**

常常想要在捕获一个异常后抛出另外一个异常，并且希望把原始异常信息保存下来，这就是异常链。在JDK1.4以后，Throwable子类在构造器中可以接受一个`cause`对象作为参数，表示原始异常，通过这样把原始异常传递给新的异常，使得即使在当前位置创建并抛出了新的异常，也能通过这个异常链追踪到异常最初发生的位置。

但在Throwable子类中，只有`Error、Exception、RuntimeException`三类异常提供了带cause参数的构造器，其他类型的异常则需要通过initCause()方法。例如定义了CustomException类，可以这样使用：

```java
CustomException cmex = new CustomException();
cmex.initCause(new NullPointerException)；
throw cmex;
```

这样一来，CustomException继承自Exception或RuntimeException，就属于自定义异常了。

一般来说，自定义异常在使用中要注意以下情况：

1. 将检查型异常转换为非检查型异常
2. 在产生异常时封装上下文信息、定义异常码、收集环境对象，有利于信息的传递
3. 在知道该如何处理的情况下才捕获异常
4. 自定义异常类型，用以封装所有的检查型异常
5. 在程序的边界进行异常捕获。如服务器相对应客户端的请求，在出口处统一catch内部异常，以免暴露服务端敏感信息
6. 只针对异常的情况才使用。不要在所有的代码中习惯性加try-catch，因为影响性能
7. 抛出与抽象相对的异常。如果方法抛出的异常与它执行的任务没有明显的联系，这中情况会让人不知所措。为了避免这个问题，更高层的实现应该捕获底层异常，同时抛出可以按照高层抽象进行解释的异常，这种做法被称为异常转译（exception translation）。高层通常提供访问方法（Throwable.getCause）来获得底层的异常。
8. 每个方法抛出的异常要有文档描述。利用javadoc的@throws标记，记录抛出每个异常的条件。如果一个方法可能抛出多个异常，不要使用异常类的某个超类。如不要声明一个方法“throw Exception”或“throw Throwable”，这将没有任何指导信息。



## Predicate接口的使用

这个接口可以理解为Java函数式编程的典范，可以上一下接口源码：

```java
public interface Predicate<T> {
    /**
     * Evaluates this predicate on the given argument.
     */
    boolean test(T t);

    /**
     * Returns a composed predicate that represents a short-circuiting logical
     * AND of this predicate and another.  When evaluating the composed
     * predicate, if this predicate is {@code false}, then the {@code other}
     * predicate is not evaluated.
     */
    default Predicate<T> and(Predicate<? super T> other) {
        Objects.requireNonNull(other);
        return (t) -> test(t) && other.test(t);
    }

    /**
     * Returns a predicate that represents the logical negation of this
     * predicate.
     */
    default Predicate<T> negate() {
        return (t) -> !test(t);
    }

    /**
     * Returns a composed predicate that represents a short-circuiting logical
     * OR of this predicate and another.  When evaluating the composed
     * predicate, if this predicate is {@code true}, then the {@code other}
     * predicate is not evaluated.
     */
    default Predicate<T> or(Predicate<? super T> other) {
        Objects.requireNonNull(other);
        return (t) -> test(t) || other.test(t);
    }

    /**
     * Returns a predicate that tests if two arguments are equal according
     * to {@link Objects#equals(Object, Object)}.
     */
    static <T> Predicate<T> isEqual(Object targetRef) {
        return (null == targetRef)
                ? Objects::isNull
                : object -> targetRef.equals(object);
    }
}
```

Predicate是个断言式的接口，其参数是<T, boolean>，也就是给一个参数T，返回boolean类型的结果。Predicate的具体实现也是根据传入的lambda表达式来决定的。

```java
boolean test(T t);
```

三个方法：`and`、`or`、`negate`，这三个方法分别对应java三个连接符号`&&、||、!`

下面有一段代码：

```java
int[] numbers= {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
		List<Integer> list=new ArrayList<>();
		for(int i:numbers) {
			list.add(i);
		}
		Predicate<Integer> p1=i->i>5;
		Predicate<Integer> p2=i->i<20;
		Predicate<Integer> p3=i->i%2==0;
		List test=list.stream().filter(p1.and(p2).and(p3)).collect(Collectors.toList());
		System.out.println(test.toString());
/** print:[6, 8, 10, 12, 14]*/
```

定义了三个断言p1，p2，p3。现在有一个从1~15的list，我们需要过滤这个list。上述的filter是过滤出所有大于5小于20，并且是偶数的列表。

假如突然我们的需求变了，我们现在需要过滤出奇数。那么我们不可能直接去改Predicate，因为实际项目中这个条件可能在别的地方也要使用。那么此时我只需要修改filter中的Predicate条件。

```java
List test=list.stream().filter(p1.and(p2).and(p3.negate())).collect(Collectors.toList());
/** print:[7, 9, 11, 13, 15]*/
```

我们直接对p3这个条件取反就可以实现了。

其实，上面的例子并不是十分贴切，取自互联网。

而实际我们工程中，用到Predicate的地方，通常都是判断的过程和逻辑基本相似，可能只有某个条件，是不一致的。我们会将这个条件用lambda表达式，将处理逻辑传入Predicate，以达到减少重复代码的效果，这里我就不一一展示代码了。

此外，Predicate的函数式设计哲学，可以将T类型所包含的业务逻辑和Predicate所表示的filter逻辑有效的解耦开来。



## servlet/tomcat/spring之间的关系

用Java有一个很大的好处，就是不管程序员自身水平有多烂，仍然可以写出非常出轨的代码。

很多人，用了很久的spring，或者tomcat，都不知道这其中他们是什么关系，如何配合运作的。

在这里，不得不上一点冷知识。

首先我们看servlet，可以尝试打开一个servlet的源码看一下，其实servlet就是一个接口。接口就是规定了一些规范，使得一些具有某些共性的类都能实现这个接口，从而都遵循某些规范（**这里我想引出另外一些思考--来自互联网**）。

有的人往往以为就是servlet直接处理客户端的http请求，其实并不是这样，servlet并不会去监听8080端口，或者直接与客户端打交道。直接和客户端（其实是监听8080端口）打交道的是“容器”，比如常用的tomcat。

客户端的请求是直接打到tomcat，它监听端口，请求过来后，根据url等信息，确定要将请求交给哪个servlet去处理，然后调用哪个servlet的service方法，service方法返回一个response对象，tomcat再把这个response返回给客户端。下面有一张图，非常好理解：

![image-20210107234617694](/Users/ethancao/notebook/NoteBook/java/img//image-20210107234617694.png)

所以，简单理解servlet，可以认为servlet就是tomcat中用于处理具体业务的**Handler**。

而servlet的接口中，处理业务的核心接口是**`service()`**接口。

**这里我们需要知道的是，每一个servlet在tomcat的容器里面，只存在一个实例**

那么，tomcat是如何处理并发请求的呢？答案就是**多线程**，而tomcat会起一个线程池去处理并发请求，这个线程池是可以设置的。

因此，在多线程下，`线程安全`的问题，自然而然就产生了（**多个线程同时访问service()接口**）。那么存在哪些场景会涉及线程安全呢？

- 如果service()方法没有访问servlet的成员变量，也没有访问全局的资源--比如静态变量、文件、数据库连接等，而只是使用了当前线程自己的资源，比如非指向全局资源的临时变量、request和response对象等。该方法是线程安全的，不必进行任何的同步控制。
- 如果service()方法访问了servlet的成员变量，但是对该变量只是读取操作，那该方法线程安全。
- 如果service()方法访问了servlet的成员变量，并进行了变量写操作，那么通常需要加上同步控制语句。
- 如果service()方法访问了全局静态变量，如果同意时刻系统中也可能有其他线程访问该静态变量，如果有读有写，通常需要加上同步控制语句。
- 如果service()方法访问了全局的资源，比如文件、数据库连接等，通常需要加上同步控制语句。

这就是所谓的**半同步半异步**网络编程模型，这样做，有以下几点好处：

1. servlet单实例，减少了产生servlet的开销
2. 通过线程池来响应多个请求，提高了请求的响应时间
3. servlet容器并不关心到达servlet请求访问，是否是同一个servlet还是另一个servlet，直接分配线程处理
4. 每一个请求由servletRequest对象来接受请求，由ServletResponse对象来响应请求，标准化

最后，怎么理解spring和上面两者之间的关系？

一句话解释：**任何spring web的entry point，都是servlet**。只是spring又做了一些花里胡哨的封装，让你更加不敢出轨撸码。

这样，就基本上清楚了。

