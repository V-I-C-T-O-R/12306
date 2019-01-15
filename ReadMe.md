12306
=======
###### 鉴于市场上的大多数抢票软件的安全问题和效率问题，就手动修改了开源的代码来为自己赢得捡漏的机会，谁叫本电脑是linux系统呢。缩减刷新的频率也是一种策略，哈哈！！！  
* 这是一款工具
* 这是一款抢票工具
* 这是一款[12306](http://www.12306.cn/)自动抢票开源工具
* 这是一款[12306](http://www.12306.cn/)自动抢票开源工具基础上优化更改的捡漏器

#### Usage
1. 在[configure.py](https://github.com/V-I-C-T-O-R/12306/blob/master/configure.py)中配置信息：  
 * 身份信息
 * 车票信息
 * 订票策略
 * 邮件配置
 * 短信配置
 * 线程池/进程池策略
 * IP池策略

2. 执行[funckeverything.py](https://github.com/V-I-C-T-O-R/12306/blob/master/fuckeverything.py)。

#### Notice
需要额外安装的第三方库:
* [requests](https://github.com/requests/requests)
* [Pillow](https://github.com/python-pillow/Pillow)
* [PrettyTable](https://github.com/lmaurits/prettytable)
* [colorama](https://github.com/tartley/colorama)
* twilio
* threadpool
* multiprocessing

#### 新功能
* 新增自动url变更请求
* 手动输入/自动识别验证码调用(调用免费接口)
* 抢票成功邮件发送
* 抢票成功短信发送[twilio](https://cuiqingcai.com)
* 内部Ip池嵌入(最近ip老是被封,不得不换个策略,更改开源ip池的源码嵌入本项目),ip池已持久化到sqlite
* sqlite数据支持
* 多线程ip池检查支持
* 多进程ip池检查支持
* 内部流程优化，新增港铁西九龙站
* 23点-6点定时睡觉

#### 你可以做啥
* 要改成多线程多进程随你咯
* 添加自己的代理池随你咯
* 添加多账户支持随你咯
* 方便个人，不为盈利
* oh! 对了，现在是2019年了，加油！

    买个票真不容易...

效果图如下：
买票  
![12306-1](https://github.com/V-I-C-T-O-R/12306/blob/master/1.png)

短信  
![sms](https://github.com/V-I-C-T-O-R/12306/blob/master/3.jpg)

###### 提示
* 借鉴了[EasyTrain](https://github.com/Why8n/EasyTrain "EasyTrain")库的代码
* 借鉴了[proxy_pool](https://github.com/jhao104/proxy_pool "proxy_pool")库的代码
* 优化当前代码和流程
