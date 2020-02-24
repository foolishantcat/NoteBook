# Maven

## settings.xml

maven设置，包含global和user两个级别的设置。

前者位于：`The Maven install: ${maven.home}/conf/settings.xml`

后者位于：`A user’s install: ${user.home}/.m2/settings.xml`

两者如果都设置了，将会合并两个xml文件的配置，重复的部分user会覆盖global设置

IntelliJ idea指定：`Preferences->Build,Execution,Deployment->Build Tools->Maven->User settings file`

## Plugins

### compiler

用于指定编译器，比较常见的设置如下：

```xml
<project>
  [...]
  <build>
    [...]
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.8.1</version>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
    </plugins>
    [...]
  </build>
  [...]
</project>
```

`version` 用于指定compiler插件的版本

如果你需要使用java8特性，那么你需要制定source为1.8。同样的，如果你需要编译出来的class文件适配JVM1.8，那么target你也需要指定为1.8。默认情况下，source和target都为1.6。

### Jar

该插件支持maven打包一个jar包，比较常见的设置如下；

```xml
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.2.0</version>
        <configuration>
          <archive>
            <manifestFile>${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
          </archive>
        </configuration>
        ...
      </plugin>
    </plugins>
  </build>
  ...
</project>
```

比较重要的标签就是`archive`，比较常见的标签如下；

```xml
<archive>
  <addMavenDescriptor/>
  <compress/>
  <forced/>
  <index/>
  <pomPropertiesFile/>
 
  <manifestFile/>
  <manifest>
    <addClasspath/>
    <addDefaultEntries/>
    <addDefaultImplementationEntries/>
    <addDefaultSpecificationEntries/>
    <addBuildEnvironmentEntries/>
    <addExtensions/>
    <classpathLayoutType/>
    <classpathPrefix/>
    <customClasspathLayout/>
    <mainClass/>
    <packageName/>
    <useUniqueVersions/>
  </manifest>
  <manifestEntries>
    <key>value</key>
  </manifestEntries>
  <manifestSections>
    <manifestSection>
      <name/>
      <manifestEntries>
        <key>value</key>
      </manifestEntries>
    <manifestSection/>
  </manifestSections>
</archive>
```

`addMavenDecriptor`决定是否生成jar包的是否生成如下两个描述文件：

```shell
META-INF/maven/${groupId}/${artifactId}/pom.xml
META-INF/maven/${groupId}/${artifactId}/pom.properties
```

默认为`true`

其中比较重要的就是`manifest`标签，比较常见的子标签含义：

`addClasspath`是否生成`Class-Path`，默认为`false`

`classpathPrefix`设置`Class-Path`的前缀，默认为""

`mainClass`设置`Main-Class`为主函数入口

### assembly

`assembly`插件主要用于允许用户搜集项目输出，类似依赖jar包，模块，文档，并输出到一个部署归档文件。

当前允许的归档文件格式：

```text
zip
tar
tar.gz (or tgz)
tar.bz2 (or tbz2)
tar.snappy
tar.xz (or txz)
jar
dir
war
```

`assembly`配置描述语法：

```xml
<project>
  [...]
  <build>
    [...]
    <plugins>
      <plugin>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.2.0</version>
        <configuration>
          <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
          </descriptorRefs>
        </configuration>
        <executions>
          <execution>
            <id>make-assembly</id> <!-- this is used for inheritance merges -->
            <phase>package</phase> <!-- bind to the packaging phase -->
            <goals>
              <goal>single</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      [...]
</project>
```

使用`assembly`方法

- 选择或者写一个`assembly`描述文件
- 在项目的根`pom.xml`文件中配置使用`assembly`插件
- 命令行/项目中运行`mvn assembly:single`

`assembly`的文件形式：

```xml
<assembly xmlns="http://maven.apache.org/ASSEMBLY/2.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/ASSEMBLY/2.0.0 http://maven.apache.org/xsd/assembly-2.0.0.xsd">
  <id/>
  <formats/>
  <includeBaseDirectory/>
  <baseDirectory/>
  <includeSiteDirectory/>
  <containerDescriptorHandlers>
    <containerDescriptorHandler>
      <handlerName/>
      <configuration/>
    </containerDescriptorHandler>
  </containerDescriptorHandlers>
  <moduleSets>
    <moduleSet>
      <useAllReactorProjects/>
      <includeSubModules/>
      <includes/>
      <excludes/>
      <sources>
        <useDefaultExcludes/>
        <outputDirectory/>
        <includes/>
        <excludes/>
        <fileMode/>
        <directoryMode/>
        <fileSets>
          <fileSet>
            <useDefaultExcludes/>
            <outputDirectory/>
            <includes/>
            <excludes/>
            <fileMode/>
            <directoryMode/>
            <directory/>
            <lineEnding/>
            <filtered/>
          </fileSet>
        </fileSets>
        <includeModuleDirectory/>
        <excludeSubModuleDirectories/>
        <outputDirectoryMapping/>
      </sources>
      <binaries>
        <outputDirectory/>
        <includes/>
        <excludes/>
        <fileMode/>
        <directoryMode/>
        <attachmentClassifier/>
        <includeDependencies/>
        <dependencySets>
          <dependencySet>
            <outputDirectory/>
            <includes/>
            <excludes/>
            <fileMode/>
            <directoryMode/>
            <useStrictFiltering/>
            <outputFileNameMapping/>
            <unpack/>
            <unpackOptions>
              <includes/>
              <excludes/>
              <filtered/>
              <lineEnding/>
              <useDefaultExcludes/>
              <encoding/>
            </unpackOptions>
            <scope/>
            <useProjectArtifact/>
            <useProjectAttachments/>
            <useTransitiveDependencies/>
            <useTransitiveFiltering/>
          </dependencySet>
        </dependencySets>
        <unpack/>
        <unpackOptions>
          <includes/>
          <excludes/>
          <filtered/>
          <lineEnding/>
          <useDefaultExcludes/>
          <encoding/>
        </unpackOptions>
        <outputFileNameMapping/>
      </binaries>
    </moduleSet>
  </moduleSets>
  <fileSets>
    <fileSet>
      <useDefaultExcludes/>
      <outputDirectory/>
      <includes/>
      <excludes/>
      <fileMode/>
      <directoryMode/>
      <directory/>
      <lineEnding/>
      <filtered/>
    </fileSet>
  </fileSets>
  <files>
    <file>
      <source/>
      <outputDirectory/>
      <destName/>
      <fileMode/>
      <lineEnding/>
      <filtered/>
    </file>
  </files>
  <dependencySets>
    <dependencySet>
      <outputDirectory/>
      <includes/>
      <excludes/>
      <fileMode/>
      <directoryMode/>
      <useStrictFiltering/>
      <outputFileNameMapping/>
      <unpack/>
      <unpackOptions>
        <includes/>
        <excludes/>
        <filtered/>
        <lineEnding/>
        <useDefaultExcludes/>
        <encoding/>
      </unpackOptions>
      <scope/>
      <useProjectArtifact/>
      <useProjectAttachments/>
      <useTransitiveDependencies/>
      <useTransitiveFiltering/>
    </dependencySet>
  </dependencySets>
  <repositories>
    <repository>
      <outputDirectory/>
      <includes/>
      <excludes/>
      <fileMode/>
      <directoryMode/>
      <includeMetadata/>
      <groupVersionAlignments>
        <groupVersionAlignment>
          <id/>
          <version/>
          <excludes/>
        </groupVersionAlignment>
      </groupVersionAlignments>
      <scope/>
    </repository>
  </repositories>
  <componentDescriptors/>
</assembly>
```

几个比较常用标签的含义如下：

`id`用于为打包的归档文件设置一个特殊的名称

`includeBaseDirectory`是否在最后的归档文件添加一个根目录，假如设置`fasle`，则unzip会把归档文件直接解压到当前文件夹

`formats/format*`指定归档文件的格式

`dependencySets/dependencySet*`指定哪些依赖会被打包进入归档文件，**但是这个不太好用，会把所有依赖包都拷贝到归档文件根节点，替代方式使用dependency插件更好**

`fileSets/fileSet*`指定哪些文件会被打包进入归档文件

其中，`fileSet`具体子标签描述如下：

`directory`设置该子模块的绝对或者相对路径

`outputDirectory`设置当前子模块的输出位于归档文件的相对位置

`includes/include*`设置一些文件类型被打包进归档文件，假如不设置，默认为所有文件

### dependencies

用于编译环节处理依赖包，具体形似如下：

```xml
<project>
  [...]
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-dependency-plugin</artifactId>
        <version>3.1.1</version>
        <executions>
          <execution>
            <id>copy-dependencies</id>
            <phase>package</phase>
            <goals>
              <goal>copy-dependencies</goal>
            </goals>
            <configuration>
              <outputDirectory>${project.build.directory}/libs</outputDirectory>
              <overWriteReleases>false</overWriteReleases>
              <overWriteSnapshots>false</overWriteSnapshots>
              <overWriteIfNewer>true</overWriteIfNewer>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
  [...]
</project>
```

比较常用需要修改的节点是`outputDirectory`，用于修改依赖包被拷贝到的地址。该插件结合`assembly`插件的`fileSet`将项目依赖包打包到归档文件。

## Run

```shell
# 清理target文件
$ mvn clean
# 编译
$ mvn compile
# 打包
$ mvn package
```




