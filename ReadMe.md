12306
=======
###### 鉴于市场上的大多数抢票软件的安全问题和效率问题，就手动修改了开源的代码来为自己赢得捡漏的机会，谁叫本电脑是linux系统呢。缩减刷新的频率也是一种策略，哈哈！！！  
* 这是一款工具
* 这是一款抢票工具
* 这是一款[12306](http://www.12306.cn/)自动抢票开源工具
* 这是一款[12306](http://www.12306.cn/)自动抢票开源工具基础上优化更改的捡漏器

#### Usage
1. pip install -r requirements.txt安装所有依赖(Python3)

2. 在[configure.py](https://github.com/V-I-C-T-O-R/12306/blob/master/configure.py)中配置信息：
 * 身份信息
 * 车票信息
 * 订票策略
 * 邮件配置
 * 短信配置
 * 线程池/进程池策略
 * IP池策略
 * 识别验证码策略

3. 执行[funckeverything.py](https://github.com/V-I-C-T-O-R/12306/blob/master/fuckeverything.py)。

#### Notice
* 鉴于本工具就是个工具，直接再做一个CNN类的训练服务不大实际(穷->服务器<=0)，所以就折中选择了免费服务自己捣鼓，希望对其他人会有启发
* 捣鼓了一个自动识别验证码的机制，当前还不是很成熟，有需要的可以酌情修改。
  当前依赖百度图像识别工具/Tencent图像识别工具，免费次数有限，你懂的
* 如果要使用捣鼓方式，请自行注册使用Baidu/Tencent AI服务
* 刷票频次最好不要太快，或许2秒最佳，哈哈
* 代码规范暂不是很好，请忽略-_-
* IP池和登录方式酌情修改
* 有坑必踩，都是为了回家

#### 新功能
* 新增自动url变更请求
* 手动输入/自动识别验证码调用
* 自己捣鼓的验证码识别方法(识别率比较低,请酌情使用并修改)
* 抢票成功邮件发送
* 抢票成功短信发送twilio[使用说明](https://cuiqingcai.com/5696.html)
* 内部Ip池嵌入(最近ip老是被封，不得不换个策略，更改开源ip池的源码嵌入本项目)，ip池已持久化到sqlite
* sqlite数据支持
* 腾讯AI个人图像识别支持(识别率比较低,服务不稳定)
* 百度AI个人图像识别支持(识别率比较低)
* 多线程ip池检查支持
* 多进程ip池检查支持
* 内部流程优化，新增港铁西九龙站/重庆西站/原平西站
* 23点-6点定时睡觉

#### 你可以做啥
* 要改成多线程多进程随你咯
* 添加自己的代理池随你咯
* 添加多账户支持随你咯
* 方便个人，不为盈利
* oh! 对了，现在是2019年了，加油！

    买个票真不容易...
##### 希望用工具抢到票的童鞋可以留个足迹，以资鼓励，发布地址:[issue](https://github.com/V-I-C-T-O-R/12306/issues/6)

效果图如下：
买票  
![12306-1](https://github.com/V-I-C-T-O-R/12306/blob/master/1.png)

短信  
![sms](https://github.com/V-I-C-T-O-R/12306/blob/master/3.jpg)

###### 提示
* 借鉴了[EasyTrain](https://github.com/Why8n/EasyTrain "EasyTrain")库的代码
* 借鉴了[proxy_pool](https://github.com/jhao104/proxy_pool "proxy_pool")库的代码
* 借鉴了其他开源代码
* 优化当前代码和流程
