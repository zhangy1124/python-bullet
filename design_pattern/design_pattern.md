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
