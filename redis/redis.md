# Redis小笔记

## 数据结构

下面介绍redis的几种基本数据结构：

**字符串（strings）**

存储证书（比如计数器）和字符串，有些公司也用来存储json/pb等序列化数据（并不推荐），浪费内存。

**哈希表（hashes）**

存储配置，对象（比如用户、商品），优点是可以存取部分key，对于经常变化的或者部分key要求atom操作的合适；

**列表（lists）**

可以用啦村最近用户状态，时间轴，有点是有序，确定是元素可重复，不去重；

**集合（sets）**

集合的有序版，很好用，对于排名之类的复杂场景可以考虑；

**位图（bitmaps）**

这个不是新增的数据类型，只是可以把字符串类型按照单个位的形似进行操作，没有实际使用过。网上很多人用bitsmaps来做活跃用户统计和用户签到功能，性能比去数据库load高很多。

**计数器（hyperloglogs）**

如名字，添加元素只记录元素个数，并不会存储元素本身，节省空间并且避免重复count，这个感觉直接用incr就可以实现；

**地理空间（geospatial indexes）**

用来做地理位置查询，如何两点之间距离，一个点附近有多少元素，合适点比较固定的场景，或者只考虑当前位置的场景，像附近的人这种就不适合，意识需要考虑某段时间内的点，而是点经常更新，压力比较大。



## 基本语法

### Hash

```shell
# 字段存在

redis> HSET site redis redis.com
(integer) 1

redis> HGET site redis
"redis.com"


# 字段不存在

redis> HGET site mysql
(nil)
```

### Set

```shell
redis 127.0.0.1:6379> SADD runoobkey redis
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mongodb
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mysql
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mysql
(integer) 0
redis 127.0.0.1:6379> SMEMBERS runoobkey

1) "mysql"
2) "mongodb"
3) "redis"
```



## 慢日志查询

在redis中，关于慢查询有两个设置--慢查询`最大超时时间`和`慢查询最大日志数`。

1. 可以通过修改配置文件或者直接在交互模式下输入一下命令来设置慢查询的时间限制，当超过这个时间，查询的记录就会加入到日志文件中。

```shell
CONFIG SET slowlog-log-slower-than num
```

设置超过多少微秒的查询为慢查询，并且将这些查询加入到日志文件中，num的单位为毫秒，windows下redis的默认查询是10000微秒即10毫秒。

2. 可以通过设置最大数量，限制日志中保存的慢查询日志的数量，此设置在交互模式下的命令如下：

```shell
CONFIG SET slowlog-max-len num
```

设置日志的最大数量，num无单位制，windows下redis默认慢查询日志的记录数量为128条。

命令解析：

`CONFIG`命令会使redis客户端自行去寻找redis的`.conf`配置文件，找到对应配置项进行修改。

**显示慢日志：**

```shell
SLOWLOG GET num
```

显示多少条慢日志

```shell
127.0.0.1:6379> slowlog get 10
1) 1) (integer) 3
   2) (integer) 1588056493
   3) (integer) 179280
   4) 1) "setbit"
      2) "aaa"
      3) "4294967295"
      4) "1"
   5) "127.0.0.1:51963"
   6) ""
```

记录中1、2、3、4分别表示：

1. 表示慢日志唯一标识符uuid
2. 命令执行时系统的时间戳
3. 命令执行的时长，以**`微秒`**来计算
4. 命令和命令的参数

做日志查询的时候，可以通过3）来查看是具体的命令运行时间（注意：再强调一次，时间的单位是微秒，但对于一个插入操作来说，10000微秒，也就是10毫秒即0.01秒已经可以算是慢慢操作了）哪些操作除了问题。当然这只限于测试使用，如果需要当业务出现redis插入查询缓慢的时间，需要去查看redis生成的持久型日志，还需要额外去配置一些内容，其中涉及到了集群和分布式，这里先点到为止。



## 异常处理

Redis发生异常

```text
WRONGTYPE Operation against a key holding the wrong kind of value
```

发生这个异常的原因大概就是你的当前程序中key的操作类型，并不与redis中存在的key的类型相匹配

举个例子：

```shell
SADD bbs "discuz.net"	// 向一个key为bbs的集合中添加了一个元素
HSET bbs website "www.g.cn"	// 向key为bbs的website域中添加了一个元素
SCARD key, gg	// 这个时候就会出如上异常，按理来说第二部就应该抛出异常
```

另外一种情况：

```shell
HSET x123 name "ethancao"	// 该案例key为简短英文加数字，redis也会抛出异常
```

解决这种冲突的方式：

1. 把之前的key删除掉，这样做当然很不好，如果你在使用公司的redis，很有可能是和同事取的key名重复了
2. 所以最好不要使用纯数字来作为key，我们可以申明一个前缀，比如：拼接上你的程序名，业务名，然后再加上你的key的唯一id，当你要get这个key的时候，同样拼接上声明的key前缀，再去取value值

同理，再给密码加密时，通常不直接使用md5直接对密码加密，而是通过生成uuid构造一个盐值（前缀或者后缀拼接潜入到密码中），然后再对字符串md5加密

## 安全漏洞处理

### 弱密码

`redis.conf`文件，修改`requirepass {复杂密码}`

### 禁止所有主机可访问

1. `redis.conf`文件，设置`bind 127.0.0.1`只允许当前主机访问
2. 配合iptables对源IP进行防火墙限制，只允许白名单里面的IP访问redis端口

```shell
// accept
## iptables -A INPUT -p tcp -s 127.0.0.1 --dport 2020 -j ACCEPT
## iptables -A INPUT -p udp -s 127.0.0.1 --dport 2020 -j ACCEPT


// drop
## iptables -I INPUT -p tcp --dport 2020 -j DROP
## iptables -I INPUT -p udp --dport 2020 -j DROP

// 保存规则并重启 iptables
## service iptables save
## service iptables restart
```



