import random

loginUrls = {
    'normal': {
        'init': {
            'url': r'https://kyfw.12306.cn/otn/login/init',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'captcha': {
            'url': r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{}'
                .format(random.random()),
            'method': 'GET',
            'response': 'binary',
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/passport/captcha/captcha-check',
            'method': 'POST',
            'headers': {
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/login/init',
            }
        },
        'login': {
            'url': r'https://kyfw.12306.cn/passport/web/login',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-Requested-With': 'xmlHttpRequest',
                'Referer': 'https://kyfw.12306.cn/otn/login/init',
            }
        },
        'userLogin': {
            'url': r'https://kyfw.12306.cn/otn/login/userLogin',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://kyfw.12306.cn/otn/login/init',
            },
            'response': 'html',
        },
        'userLoginRedirect': {
            'url': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'method': 'GET',
            'response': 'html',
        },
        'uamauthclient': {
            'url': r'https://kyfw.12306.cn/otn/uamauthclient',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'checkUser': {
            'url': r'https://kyfw.12306.cn/otn/login/checkUser',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'loginOut': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/index/initMy12306',
            },
            'response': 'html',
        },

    },
    # --------------------------------------------------------------------------------------------------------
    'other': {
        'init': {
            'url': r'https://kyfw.12306.cn/otn/login/init',
            'method': 'GET',
            'headers': {
                'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                r'Content-Type': r'application/x-www-form-urlencoded',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
        'uamtk': {
            'url': r'https://kyfw.12306.cn/passport/web/auth/uamtk',
            'method': 'POST',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': r'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            }
        },
        'captcha': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&rand=sjrand&{}'
                .format(random.random()),
            'method': 'GET',
            'response': 'binary',
        },
        'captchaCheck': {
            'url': r'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
            'method': 'POST',
            'headers': {
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            }
        },
        'login': {
            'url': r'https://kyfw.12306.cn/otn/login/loginAysnSuggest',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'Origin': r'https://kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            }
        },
        'loginOut': {
            'url': r'https://kyfw.12306.cn/otn/login/loginOut',
            'method': 'GET',
            'headers': {
                r'Content-Type': r'application/x-www-form-urlencoded',
                'Host': r'kyfw.12306.cn',
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
            },
            'response': 'html',
        },
    },
}

autoVerifyUrls = {
    '12305':{
        'url':'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&'.format(
            random.random()),
        'method':'GET'
    },
    'api':{
        'url':'https://12306.jiedanba.cn/api/v2/getCheck',
        'method':'POST',
        'headers': {'Content-Type': 'application/json'}
    },
    'img_url':{
        'url':'https://check.huochepiao.360.cn/img_vcode',
        'method':'POST'
    },
    'check_url':{
        'url':'https://kyfw.12306.cn/passport/captcha/captcha-check',
        'method':'GET'
    },
    "origin_url":"https://12306.jiedanba.cn/"
}

queryUrls = {
    'query': {
        'url': r'https://kyfw.12306.cn/otn/leftTicket/query',
        'method': 'GET',
        'headers': {
            'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
        }
    },
}
submitUrls = {
    'dc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': r'kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'queryMyOrderNoComplete': {
            'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
            },
        }

    },
    'wc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': r'kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            'method': 'GET',
            'response': 'html',
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmGoForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initWc',
            },
        },
        'queryMyOrderNoComplete': {
            'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
            },
        }

    }
}

tencent_api = {
    # 基本文本分析API
    "nlp_wordseg": {
        'APINAME': '分词',
        'APIDESC': '对文本进行智能分词识别，支持基础词与混排词粒度',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordseg',
        'APIPARA': 'text'
    },
    "nlp_wordpos": {
        'APINAME': '词性标注',
        'APIDESC': '对文本进行分词，同时为每个分词标注正确的词性',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordpos',
        'APIPARA': 'text'
    },
    'nlp_wordner': {
        'APINAME': '专有名词识别',
        'APIDESC': '对文本进行专有名词的分词识别，找出文本中的专有名词',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordner',
        'APIPARA': 'text'
    },
    'nlp_wordsyn': {
        'APINAME': '同义词识别',
        'APIDESC': '识别文本中存在同义词的分词，并返回相应的同义词',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordsyn',
        'APIPARA': 'text'
    },

    # 计算机视觉--OCR识别API
    "ocr_generalocr": {
        'APINAME': '通用OCR识别',
        'APIDESC': '识别上传图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr',
        'APIPARA': 'image'
    },
    "ocr_handwritingocr": {
        'APINAME': '手写OCR识别',
        'APIDESC': '识别上传图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr',
        'APIPARA': 'image'
    },
    "ocr_idcardocr": {
        'APINAME': '身份证OCR识别',
        'APIDESC': '识别身份证图像上面的详细身份信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_idcardocr',
        'APIPARA': 'image,card_type'
    },
    "ocr_bcocr": {
        'APINAME': '名片OCR识别',
        'APIDESC': '识别名片图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_bcocr',
        'APIPARA': 'image'
    },
    "ocr_driverlicenseocr": {
        'APINAME': '行驶证驾驶证OCR识别',
        'APIDESC': '识别行驶证或驾驶证图像上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_driverlicenseocr',
        'APIPARA': 'image,type'
    },
    "ocr_bizlicenseocr": {
        'APINAME': '营业执照OCR识别',
        'APIDESC': '识别营业执照上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_bizlicenseocr',
        'APIPARA': 'image'
    },
    "ocr_creditcardocr": {
        'APINAME': '银行卡OCR识别',
        'APIDESC': '识别银行卡上面的字段信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_creditcardocr',
        'APIPARA': 'image'
    },
    # 物体识别--OCR识别API
    "vision_objectr": {
        'APINAME': '物体OCR识别',
        'APIDESC': '对图片进行物体识别，快速找出图片中包含的物体信息',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/vision/vision_objectr',
        'APIPARA': 'image',
        'TENCENT_ENTITY_URL':'https://ai.qq.com/doc/vision_object.shtml'
    },
    "image_tag": {
        'APINAME': '多标签识别',
        'APIDESC': '识别一个图像的标签信息,对图像分类',
        'APIURL': 'https://api.ai.qq.com/fcgi-bin/image/image_tag',
        'APIPARA': 'image'
    },
}
