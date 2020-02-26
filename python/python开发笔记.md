# Python开发笔记

version：python3.7

## 包管理

### `__init__.py`文件作用

我们经常在python的魔窟奥目录中会看到`__init__.py`这个文件，那么它到底有什么作用呢？

1. 标识目录是一个python的模块包（module package）

如果你是使用python的相关IDE（PyCharm）来进行开发，那么如果目录中存在该文件，该目录就会被识别为 **model package**

2. 简化模块导入操作：

实际上，如果目录中包含了`__init__.py`时，当用`import`导入该目录时，会执行`__init__.py`里面的代码（且仅会执行）。

此外，在使用`from package import *`的时候，会导入包中所有内容

我们通常会使用`*`表示导入包中的所有内容

这是怎么实现的呢？`__all__`变量就是干这个工作的。

> package
>
> `__init__.py`
>
> > package1
> >
> > > `__init__.py`
> > >
> > > test1.py
> >
> > package2
> >
> > > `__init__.py`
> > >
> > > test2.py
> >
> > package3
> >
> > > `__init__.py`
> > >
> > > test3.py
> >
> > test4.py

```python
# __init__.py
__all__ = ["package1", "package2"]
```

等价于：

```python
from package import package1, package2
```

我们会发现`package3`并没有被导入

此外，`from package import *`会导致继续查找`package1`和`package2`中的`__init__.py`并执行

同理，如果使用`from package import package3`，会导致package的`__init__.py`和package3中`__init__.py`以及`test4.py`中的一级代码依次被执行

3. 配置模块的初始化操作

基于以上描述，应该能够理解该文件就是一个正常的python代码文件。

因此可以将模块的初始化代码放入该文件中

## 包下载

离线下载安装包，并离线安装

```shell
# 将包下载到本地
$ pip download third-packge==version -d "."
# 安装包
$ pip install third-packege.tar.gz/whl
```



## 打包和发布

参考地址：

https://packaging.python.org/tutorials/packaging-projects/

```shell
python setup.py sdist bdist_wheel
pip install dist/***.tar.gz
```

