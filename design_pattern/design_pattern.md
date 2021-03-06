# 设计模式

## 1. 抽象工厂模式

**角色:** 

1. AbstractFactory: 抽象工厂
2. ConcreteFactory: 具体工厂
3. AbstractProduct: 抽象产品
4. Product: 具体产品

**适用场景:**

- 一个系统要独立于它的产品的创建、组合和表示时。
- 一个系统要由多个产品系列中的一个来配置时。
- 需要强调一系列相关的产品对象的设计以便进行联合使用时。
- 提供一个产品类库，而只想显示它们的接口而不是实现时。

**优点：**

1. 具体产品从客户代码中被分离出来
2. 容易改变产品的系列
3. 将一个系列的产品族统一到一起创建

**缺点:**

1. 在产品族中扩展新的产品是很困难的，它需要修改抽象工厂的接口

**参考:**

> [1]. http://design-patterns.readthedocs.io/zh_CN/latest/creational_patterns/abstract_factory.html

> [2]. https://zh.wikipedia.org/wiki/%E6%8A%BD%E8%B1%A1%E5%B7%A5%E5%8E%82


## 2. 单例模式

**实现单例模式的思路:**

一个类能返回对象一个引用(永远是同一个)和一个获得该实例的方法（必须是静态方法，通常使用getInstance这个名称）；当我们调用这个方法时，如果类持有的引用不为空就返回这个引用，如果类保持的引用为空就创建该类的实例并将实例的引用赋予该类保持的引用；同时我们还将该类的构造函数定义为私有方法，这样其他处的代码就无法通过调用该类的构造函数来实例化该类的对象，只有通过该类提供的静态方法来得到该类的唯一实例。

单例模式在多线程的应用场合下必须小心使用。如果当唯一实例尚未创建时，有两个线程同时调用创建方法，那么它们同时没有检测到唯一实例的存在，从而同时各自创建了一个实例，这样就有两个实例被构造出来，从而违反了单例模式中实例唯一的原则。 解决这个问题的办法是为指示类是否已经实例化的变量提供一个互斥锁(虽然这样会降低效率)。

**参考：**

> [1]. https://zh.wikipedia.org/wiki/%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F
