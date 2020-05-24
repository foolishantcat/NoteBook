# sklearn学习笔记

当前机器学习和人工智能风口浪尖，深处一个AI团队，虽然我只是一枚小小的后台开发，也免不了想学习一把机器学习，鉴于团队都在用sklearn，所以就从sklearn开始吧。

首先，为啥要使用sklearn，而不是tensorflow呢？

sklearn貌似在小数据集上，表现较之tensorflow更为简单易用。tensorflow对DNN等深度神经网络有较好的支持。

此外，假如希望模型是真“在线”访问，可以考虑一下tensorflow，因为它有一个tf-serving，基于RPC调用的在线服务。

当然，这个不是重点，你也可以随手自己用python、java或者其他语言自己搭一个服务，都是完全没问题的。whatever~

虽然之前买过两本机器学习的数，甚至连高数的坑我都回去踩了，但是缺少实战经验的我，也只是感觉自己是个小白。所以先从网上的公开数据集开始吧。

首先，sklearn是自带公开数据集的：

- 小数据集：sklearn.datasets.load_<name>
- 可在线下载的数据集: sklearn.datasets.fetch_<name>
- 计算机生成的数据集：sklearn.datasets.make_<name>
- Svmlight/libsvm格式的数据集: sklearn.datasets.load_svmlight_fie(...)
- data.org数据集：sklearn.datasets.fetch_mldata(...)

这里我们采用一个手写数据集：load_digists，这个数据集简单来说就是包含了1797个64像素的手写数字，可以在命令行打印数据集的形状（shape）：

```shell
(1797, 64)
```

机器学习，顾名思义：它需要学习，然后才能预测，以先知数据，预测未知事件。

大体demo流程：

- 加载数据集
- 划分训练数据、测试数据的大小
- 使用训练数据，训练得到模型
- 使用测试数据，预测手写数字
- 假如你喜欢，还可以画个图，或者保存一下模型

具体代码如下（我是比较烦网上那种“分段式编程”的，能不能一次给全代码，也没几行）：

```python
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
import matplotlib.pylab as plt
from sklearn import svm


def main():
    d = load_digits()
    # # 查看数据集的键名
    # d.keys()
    # # 查看手写字图片的形状
    # d.images.shape
    # # 相当于对images对象进行了降维操作
    # d.data.shape
    # # 查看手写字标签的形状
    # d.target.shape
    # # 查看第一张图片
    # plt.imshow(d.images[0])
    # 显示数据集中的第一个数字
    # plt.show()

    # 把数据集的数据和标签划分为训练集和测试集以及他们的标签
    x_train, x_test, y_train, y_test = \
        train_test_split(d.data, d.target, test_size=.25, random_state=42)

    # 设置模型参数
    svc = svm.SVC(C=100, gamma=0.001)
    # 使用训练数据，进行模型训练
    svc.fit(x_train, y_train)
    # 使用测试数据，进行预测
    y_pred = svc.predict(x_test)

    # 保存一下模型，到本地文件夹（你喜欢咯）
    # joblib.dump(svc, 'MyDigitsModel.pkl')
    # joblib也支持离线加载已经训练好的模型，感兴趣你也可以了解一下PMML
    # load_m = joblib.load('MyDigitsModel.pkl')

    # 绘制预测的图像
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    images_and_predictions = list(zip(x_test.reshape(450, 8, -1), y_pred))
    plt.figure(figsize=(14, 9))
    for i, (img, pred) in enumerate(images_and_predictions[:24], start=1):
        plt.subplot(4, 6, i, )
        plt.subplots_adjust(hspace=0.3)
        plt.axis('off')
        plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
        plt.title(f'预测值：{str(pred)}')

    plt.show()


if __name__ == '__main__':
    main()

```

以上代码中，比较重要的只有一行：

```python
svc = svm.SVC(C=100, gamma=0.001)
```

改行是模型训练的过程，可以看到有两个参数：

> C：值越大，即对误分类的惩罚增大，泛化能力弱，趋向于对训练集全分对的情况，这样对训练集测试时准确率很高；反之，值越小，对误分类的惩罚减小，允许容错，将他们当成噪声点，泛化能力较强。默认值1.0。
>
> kernel：核参数，默认是rbf，可以是‘linear’，‘poly’，‘rbf’，‘sigmoid’，‘precomputed’
>
> random_state: 数据洗牌时的种子值，int值
>
> gamma：‘rbf’，‘poly’和‘sigmoid’的核函数参数。默认是‘auto’，则会选择1/n_features
>
> probability：是否采用概率估计？默认为False
>
> tol：停止训练的误差值大小，默认为1e-3
>
> cache_size：核函数cache缓存大小，默认为200
>
> max_iter：最大迭代次数。-1为无限制

不出意外，以上代码加上合理的配置，你就可以训练出来想要的模型了。

~~我只是代码的搬运工，代码可以搬，知识还是要靠自己学~~