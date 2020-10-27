



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

被修饰的方法返回值只可能是`void`或`Feture`类型。一般来说说，会声明`ListenableFuture`或`CompletableFuture`类型，这两种类型具有更为丰富的异步任务交互体验。

当返回一个`Feture`句柄时，能够被用于追踪异步方法执行的结果。

如果在Spring里面使用Aysnc装饰器，需要在启动类加上`@EnableAsync`注释。

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