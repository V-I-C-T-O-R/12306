12306
=======
###### 鉴于2019年12306更新了抢票规则和候补策略,不管能不能帮助抢到票，都希望本工具能作为一个单点买票工具为大家在抢票思路上能做个参考

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

3. 执行[funckeverything.py](https://github.com/V-I-C-T-O-R/12306/blob/master/fuckeverything.py)
###### (ps:如果有登录验证失败次数过多,可以尝试自己抓deviceId Url来更新urls_conf.py文件中的getDevicesId对应的url。此外除了手动更改之外，可以替换train/login/Login.py中的_login_init方法中的self._handle_device_code_manual为self._handle_device_code_auto自动获取设备指纹。注：自动获取设备指纹方法容易引起12306拦截，请测试执行)

##### 希望用工具抢到票的童鞋可以留个足迹，以资鼓励，发布地址:[issue](https://github.com/V-I-C-T-O-R/12306/issues/6)

#### Notice
* 鉴于本工具就是个工具，直接再做一个CNN类的训练服务不大实际(穷->服务器<=0)，所以就折中选择了免费服务自己捣鼓，希望对其他人会有启发
* 捣鼓了一个自动识别验证码的机制，当前还不是很成熟，有需要的可以酌情修改。
  当前依赖百度图像识别工具/Tencent图像识别工具，免费次数有限，你懂的
* 如果要使用捣鼓方式，请自行注册使用Baidu/Tencent AI服务
* 刷票频次最好不要太快，但是整点发售0.2秒最佳，网速不好，延迟大还真抢不过，哈哈
* 代码规范暂不是很好，请忽略-_-
* IP池和登录方式酌情修改,短信发送twilio[使用说明](https://cuiqingcai.com/5696.html)
* 有坑必踩，都是为了回家
* 配置详情请关注configure.py文件

#### 你可以做啥
* 要改成多线程多进程随你咯
* 添加自己的代理池随你咯
* 添加多账户支持随你咯
* 方便个人，不为盈利
* oh! 对了，现在是2020年了，一般人就只能费点钱买服务买票捡漏了，加油！

    买个票真不容易...

效果图如下：
买票  
![12306-1](https://github.com/V-I-C-T-O-R/12306/blob/master/1.png)
![12306-2](https://github.com/V-I-C-T-O-R/12306/blob/master/2.png)

短信  
![sms](https://github.com/V-I-C-T-O-R/12306/blob/master/3.jpg)

###### 提示
* 借鉴了[EasyTrain](https://github.com/Why8n/EasyTrain "EasyTrain")库的代码
* 借鉴了[proxy_pool](https://github.com/jhao104/proxy_pool "proxy_pool")库的代码
* 借鉴了其他开源代码
* 优化当前代码和流程
