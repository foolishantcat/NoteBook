# Redis小笔记

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

