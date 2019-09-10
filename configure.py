# 必填
# 用户名
USER_NAME = '******@qq.com'
# 密码
USER_PWD = '******'
# 出发站
FROM_STATION = '广州'
# 到达站
TO_STATION = '新余'
# 乘车日期（格式: YYYY-mm-dd）
TRAIN_DATE = '2019-01-30'
# 购票人身份证号
PASSENGERS_ID = ['430121199711112437','430123199312133726']
# 票类型（单程:dc 往返:wc）
TOUR_FLAG = 'dc'
#订票策略,1表示必须全部一起预定，2表示可以部分提交
POLICY_BILL = 1

#cookie存放地址
COOKIE_SAVE_ADDRESS = 'cookie.txt'

# 选填
# 车次 eg:['G6343','G6212']
TRAINS_NO = ['G1404','G1402','G632']
# 座位类别（商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)）
#SEAT_TYPE_CODE = ['M', 'O', '4', '3', '2', '1']
SEAT_TYPE_CODE = ['3']
# 购票人类别（成人票:1,儿童票:2,学生票:3,残军票:4）
PASSENGER_TYPE_CODE = '1'
# 座位选择 eg:['1A','2A'],有多少张票就填多少个,其中，A靠窗，B中间，C过道,D过道,F靠窗
#解释：如果你有三个人，那么你就可以选择['1A','2A','2B']，这里的1和2代表的是排数(选座默认出现两排图形位置)。也就是'1A','2A','2B'三个元素代表3个人，A和B代表座位的位置，1和2代表的是排数
CHOOSE_SEATS = []

# 刷票间隔(单位:s)
QUERY_TICKET_REFERSH_INTERVAL = 0.3

#选择识别验证码的方式,默认1方式
# 1表示手动,2表示自动识别(调用第三方接口,已失效),3表示使用本工具自己捣鼓的验证码识别方式(配置百度ai/tencent ai账号)
SELECT_AUTO_CHECK_CAPTHCA = 1
#baidu=1/tencent=2选择,此参数只在SELECT_AUTO_CHECK_CAPTHCA = 3的情况下有效,默认为百度服务
IMAGE_OCR_SERVICE_CHOOSE = 1

#是否更新ip池，默认为不更新
IS_REFASH_IP_POOL = False
#执行检查任务的线程/进程池大小
THREAD_POOL_SIZE = 20
#采用多线程或多进程,默认多线程
THREAD_OR_PROCESS = True


mail_host = 'smtp.qq.com'
mail_user = '******@qq.com'
mail_pass = '******'
mailto_list = ['example@163.com']

#短信,使用说明：https://cuiqingcai.com/5696.html
ACCOUNT_SID = "DC4c32222717d4daa96bf8b611fd311f66"
# Your Auth Token from twilio.com/console
AUTO_TOKEN = "6b8087bf15572c210298375641f59e6a"
FROM_NUM = '(731) 201-9528'
TO_NUM = '+8618098271128'

#百度AI图像识别应用
BAIDU_APP_ID = '111111086'
BAIDU_API_KEY = 'L4NedkfjgleipGfrVM7aTiNsEr'
BAIDU_SECRET_ID = 'ujPzd234191zH*******GGskjynZXb'

#腾讯地址https://ai.qq.com/product/visionimgidy.shtml#scene坑的想哭,腾讯有两套系统,账号不互通
TENCENT_APP_ID = '31144562600'
TENCENT_SECRET_KEY = 'KzvJf8rjdus5MVLt'