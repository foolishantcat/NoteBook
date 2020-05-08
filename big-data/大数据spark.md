---
typora-root-url: ..
---

# 大数据Spark
&nbsp;&nbsp;Spark目前已经成为主流的大数据分析平台，所以熟练掌握spark的使用成为了机器学习/大数据分析领域必备的技能。

## Spark简介
目前所熟知的spark运用领域包含：
- 通用计算引擎，能够运行MapReduce、数据挖掘、图运算、流式计算、SQL等多种框架
- 基于内存，数据可存在内存中，特别适用于需要迭代多次运算的场景
- 与Hadoop继承，能够直接读写HDFS中的数据，并能运行再YARN之上

![](/big-data/img/spark-frame.png)

spark构成：
- Application		运行在集群上的用户程序，包含集群上的driver program和多个executor线程组成
- Driver program	application运行的main方法，并生成spark context
- Cluster Manager	集群资源管理器
- Deploy Model            部署模式，用于区别driver program的运行方式
++ cluster mode  集群模式，driver在集群内部启动
++ client mode    客户端模式（默认），driver进程从集群外部启动
- Worker node	      工作节点，运行application的节点
- Executor		       work node的上进程，运行task并保持数据交互，每一个application有自己的executor
- Task		运行于Executor中的任务单元，spark应用程序最终被划分为经过优化后的多个任务的集合
- Job		由多个转变构建的并行计算任务，具体为spark中的action操作，一个action就为一个job			

目前市场主流的spark编程语言：
- scala，官方推荐
- python，可以使用pyspark，对于会python的人来说上手很快

## Azkaban使用
[【以下部分内容引】](https://www.cnblogs.com/honeybee/p/7921626.html)

azkaban是一款可以通过UI调用spark进行大数据分析的开源软件平台

主页：[https://azkaban.github.io/](https://azkaban.github.io/)

github：[https://github.com/azkaban/azkaban](https://github.com/azkaban/azkaban)

azkaban的工作流中的参数可以分为如下几个类型：

|参数类型|作用域说明|
|---------:|:-----------------------|
|UI 页面输入参数 ，即工作流参数|flow全局有效|
|工作流ZIP压缩包中的属性文件|flow全局有效，zip文件目录以及子目录有效|
|工作流运行时参数|flow全局有效|
|环境变量参数|flow全局有效|
|job的common参数|job内局部有效|
|job文件中定义的参数|job内局部有效|
|上游作业传递给下游的参数|job局部有效|

## RDD介绍
以下引：[https://www.jianshu.com/p/248f3946ee31](https://www.jianshu.com/p/248f3946ee31)

​	RDD就像一个Numpy array或者一个Pandas series，可以视作一个有序的item集合

​	只不过，这些item并不存在driver端的内存里，而是被分割成很多个partitions，每个partition的数据存在集群的executor的内存中

​	在Spark里，所有的处理和计算任务都会被组织成一系列Resilient Distributed Dataset(弹性分布式数据集，简称RDD)上的transformations(转换) 和 actions(动作)。 

+ Transformations
1. map() 对RDD的每一个item都执行同一个操作
2. flatMap() 对RDD中的item执行同一个操作以后得到一个list，然后以平铺的方式把这些list里所有的结果组成新的list
3. filter() 筛选出来满足条件的item
4. distinct() 对RDD中的item去重
5. sample() 从RDD中的item中采样一部分出来，有放回或者无放回
6. sortBy() 对RDD中的item进行排序
- Action
1. collect() 计算所有的items并返回所有的结果到driver端，接着collect()会以python list的形式返回结果
2. first() 和上面是类似的，不过只返回第1个item
3. take(n) 类似，但是返回n个item
4. count() 计算RDD中item的个数
5. top(n) 返回头n个items，按照自然结果排序
6. reduce() 对RDD中的items做聚合
- 更为复杂的transformations和actions
1. reduceByKey() 对所有有着相同key的items执行reduce操作
2. groupByKey() 返回类似（key，listOfValues）元组的RDD，后面的value List是同一个key下面的
3. sortByKey() 按照key排序
4. countByKey() 按照key取对item个数进行统计
5. collectAsMap() 和collect有些类似，但是返回的是k-v的字典

## 文件读取
```python
textFile = sc.textFile("file:///usr/local/spark/mycode/wordcount/word.txt")
```
textFile是一个方法，用来加载文本数据，默认是从HDFS上加载，如果要加载本地文件，就必须使用file:///加路径的形式

## 异常列表

1. RDD对象action不能嵌套调用，比如rdd_1.map(...., func_1(rdd_2))，会异常出错
2. 不能把过于大型的数据集合从RDD转成collect，collect是放到本机内存，会导致内存超限，应该在最终结果获取环节使用collect

## Hive中Partition如何使用

一、背景

1. 在Hive select查询中一般会扫描整个表内容，会消耗很多时间做没必要的工作。有时候只需要扫描表中关心的一部分数据，因此建表时引入partition概念。

2. 分区表指的是在创建表时指定的partition的分区空间。

3. 如果需要创建有分区的表，需要在create表的时候调用可选参数partitioned by，详见表创建的语法结构。

二、技术细节

1. 一个表可以拥有一个或者多个分区，每个分区以文件夹的形式单独存在表文件夹的目录下。
2. 表和列名不区分大小写。
3. 分区是以字段的形式在表结构中存在，通过describe table命令可以查看到字段存在，但是该字段不存放实际的数据内容，仅仅是分区的标识。
4. 建表的语法（建分区可参见PARTITIONED BY参数）。
5. 分区建表分为2种，一种是单分区，也就是说在表文件夹目录下只有一级文件夹目录。另外一种是多分区，表文件夹下出现多文件夹嵌套模式。

a、单分区建表语句：`create table day_table（id int，content string）partitioned by（dt string）；`单分区表，按天分区，在表结构中存在id，content，dt三列。

b、双分区建表语句：`create table day_hour_table（id int，content string）partitioned by（dt string，hour string）；`双分区表，按天和小时分区，在表结构中新增加了dt和hour两列。

6. 添加分区表语法（表已创建，在此基础上添加分区）

```sql
ALTER TABLE table_name ADD partition_spec[LOCATION 'location1'] partition_spec[LOCATION 'location2']...partition_spec::PARTITION(partition_col = partition_col_value, partition_col = partition_col_value,...)
```

用户可以用`ALTER TABLE ADD PARTITION`来向一个表中增加分去。当分区名是字符串时加引号。例：

```sql
ALTER TABLE day_table ADD PARTITION(dt='2008-08-08', hour='08') location '/path/pv1.txt' PARTITION(dt='2008-08-08', hour='09') location '/path/pv2.txt';
```

7. 删除分区语法

```sql
ALTER TABLE day_table DROP partition_spec,partition_spec,...
```

用户可以用`ALTER TABLE DROP PARTITION`来删除分区。分区的元数据和数据将被一并删除。

例：

```sql
ALTER TABLE day_hour_table DROP PARTITION(dt='2008-08-08', hour='09');
```

8. 数据加载进分区表中语法：

```sql
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO TABLE tablename [PARTITION(partcol1=val1, partcol2=val2...)]
```

例：

```sql
LOAD DATA INPATH '/usr/pv.txt' INTO TABLE day_hour_table PARTITION(dt='2008-08-08', hour='08'); LOAD DATA local INPATH '/usr/hua/*' INTO TABLE day_hour_partition(dt='2010-07-07');
```

当数据被加载至表中时，不会对数据进行任何转换。Load操作只是将数据复制至Hive表对应的位置。数据加载时在表下自动创建一个目录，文件存放在该分区下。

9. 基于分区的查询的语句

```sql
SELECT day_table.* FROM day_table WHERE day_table.dt >= '2008-08-08';
```

10. 查看分区语句

```sql
hive> show partitions day_hour_table;
OK
dt=2008-08-08/hour=08
dt=2008-08-08/hour=09
dt=2008-08-09/hour=09
```

三、总结

1. 在Hive中，表中的一个partition对应于表下的一个目录，所有的partition的数据都存储在最字集的目录中。
2. 总的说来partition就是辅助查询，缩小查询范围，加快数据的检索速度和对数据按照一定的规格和条件进行管理。

## Hive表的源文件存储格式

hive表的源文件存格式有几类：

1. **TextFile**

默认格式，建表时不指定默认为这个格式，导入数据时会直接通过hadoop fs -cat查看

2. **SequenceFile**

一种Hadoop API提供的二进制文件，使用方便、可分割、可压缩等特点。SequenceFile将数据以<key, value>的形式序列化到文件中。序列化和反序列化使用Hadoop的标准writable接口实现。key为空，用value存放实际的值，这样可以避免map阶段的排序过程。

三种压缩选择：`NONE,RECORD,BLOCK`。Record压缩率低，一般建议使用BLOCK压缩。使用时设置参数：

```sql
SET hive.exec.compress.output=true;
SET io.seqfile.compression.type=BLOCK;
create table test2(str STRING) STORED AS SequenceFile;
```

3. **RCFile**

一种行列存储相结合的存储方式。首先，其将数据按行分块，保证同一个record在一个块上，避免读一个记录需要读取多个block。其次，块数据列式存储，有利于数据压缩和快速的列存取。

理论上具有高查询效率（但hive官方说效果不明显，只有存储上能省10%的空间，所以不好用，可以不用）。

RCFile结合`行存储`查询的快速和`列存储`节省空间的特点：

1）同一行的数据位于同一节点，因此元组重构的开销很低；

2）块内列存储，可以进行列维度的数据压缩，跳过不必要的列读取。

查询过程中，在IO上跳过不关心的列。实际过程是，在map阶段从远端拷贝仍然拷贝整个数据块到本地目录，也并不是真正直接跳过列，而是通过扫描每一个row group的头部定义来实现的。

但是在整个HDFS Block级别的头部并没有定义每个列从哪个row group起始到哪个group结束。所以在读取所有列的情况下，RCFile的性能反而没有SequenceFile高。

4. **ORC**

hive给出的新格式，属于RCFile的升级版

5. **自定义格式**

用户的数据文件格式不能被当前Hive所识别的，是通过实现inputFormat和outputFormat来自定义输入输出格式。

**注意：**

只有TextFile表能直接加载数据，必须，本地load数据，和external外部表直接加载云路径数据，都只能用TextFile表。

更深一步，hive默认支持的压缩文件（hadoop默认支持的压缩格式），也只能用TextFile表直接读取。其他格式不行。可以通过TextFile加载后insert到其他表中。

换句话说，**SequenceFile、RCFile表不能直接加载数据，**数据要首先导入到TextFile表，再从TextFile表通过**insert select from**导入到SequenceFile、RCFile表。

SequenceFile、RCFile表的源文件不能直接查看，在Hive中用select看。RCFile源文件可以用`hive --service rcfilecat /XXXXXXXXX/000000_0`查看，但是格式不同，很乱。

ORC是RCFile的升级版，性能有大幅度提升

而且数据可以压缩存储，压缩比和Lzo压缩差不多，比text文件压缩比可以达到70%的空间。而且读性能非常高，可以实现高效查询。





