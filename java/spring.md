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

用于标记一个方法可以异步执行，也可以呗用于类型级别，被这个类型锁标记的方法可以异步执行。注意，`@Async`不可以在已经被声明了`@Configuration`的类里面被使用。例如：

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

被声明了该装饰器的类型，作为一个`@ExceptionHandler`的控制器，用于处理`Controller`所产生的一场消息。

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

## SpringBootApplication

`org.springframework.boot.autoconfigure`

SpringBoot目前是和SpringFrameWork独立的包。所以需要独立饮用。

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

## corsConfigurer

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