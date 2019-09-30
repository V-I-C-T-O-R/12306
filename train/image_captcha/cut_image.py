import cv2
import os
from configure import BAIDU_API_KEY,BAIDU_APP_ID,BAIDU_SECRET_ID,TENCENT_APP_ID,TENCENT_SECRET_KEY,IMAGE_OCR_SERVICE_CHOOSE
import skimage
import numpy as np
from conf.constant import IMAGE_OCR_SERVICE_BAIDU,IMAGE_OCR_SERVICE_TENCENT
from train.image_captcha.tencent import TencentAI
from utils.Log import Log
#opencv-python模块
#scikit-image
#numpy
from train.image_captcha.baidu import ImageClassify

IMG_V_POS = [4, 76, 148, 220]
IMG_H_POS = [40, 108]
IMG_WIDTH = 68  # 每个小图片的宽度
IMG_HEIGHT = 68  # 每个小图片的高度

def read_image(fn):
    """
    得到验证码完整图像
    :param fn:图像文件路径
    :return:图像对象
    """
    im = None
    try:
        im = skimage.io.imread(fn, as_gray=False)
    except Exception:
        pass
    return im

def load_image(im, color=True):
    img = skimage.img_as_float(im).astype(np.float32)
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        if color:
            img = np.tile(img, (1, 1, 3))

    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img

def write_image(im, fn):
    skimage.io.imsave(fn, im)


def get_text(im):
    """
    得到图像中的文本部分
    """
    return im[3:24, 116:288]


# 分割图片
def get_image(im):
    img = []
    for v in range(2):  # 图片行
        for h in range(4):  # 图片列
            img.append(im[(40 + (v * 72)):(108 + (v * 72)), (4 + (h * 72)):((h + 1) * 72)])
    return img


# 二值化图像
def binarize(im):
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    (retval, dst) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    return dst

# 获取图像值

def show_image(im):
    print(im.ndim, im.dtype)
    cv2.imshow("image", im)
    cv2.waitKey(0)

# 将文件写入到
def cut_image(dir_address,img_name):
    f_name = os.path.join(dir_address , img_name)
    im = read_image(f_name)
    if im is None:
        Log.w("该图片{ %s }处理异常: " % img_name)
        return
    all_pic = dir_address + 'pic'
    write_image(get_text(im), os.path.join(all_pic, img_name))
    num = 1
    sub_name = img_name.split('.')
    for sub_im in get_image(im):
        sub_img_name = sub_name[0] + '_' + str(num) + '.' + sub_name[1]
        num += 1
        write_image(sub_im, os.path.join(all_pic, sub_img_name))

    #开始验证图片百度/Tencent
    if IMAGE_OCR_SERVICE_CHOOSE == IMAGE_OCR_SERVICE_BAIDU:
        image = ImageClassify(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_ID)
        captcha_name = image.resolve_words(os.path.join(all_pic, img_name)) or ''
    elif IMAGE_OCR_SERVICE_CHOOSE == IMAGE_OCR_SERVICE_TENCENT:
        image = TencentAI(TENCENT_APP_ID, TENCENT_SECRET_KEY)
        captcha_name = image.resolve_words(os.path.join(all_pic, img_name)) or ''

    flag_name = set(captcha_name)
    Log.w('找出:'+captcha_name)
    img_list = sorted(os.listdir(all_pic))
    results = []
    for i in img_list:
        if i == img_name:
            continue
        c_path = os.path.join(all_pic, i)
        index = int(i.split('.')[0].split('_')[1])-1
        if IMAGE_OCR_SERVICE_CHOOSE == IMAGE_OCR_SERVICE_BAIDU:
            resolve_name = image.resolve_image(c_path) or ''
        elif IMAGE_OCR_SERVICE_CHOOSE == IMAGE_OCR_SERVICE_TENCENT:
            resolve_name = image.resolve_image(os.path.join(all_pic, img_name)) or ''

        Log.w('第'+str(index)+'图片识别为:'+resolve_name)
        variable_name = set(resolve_name)
        if flag_name.intersection(variable_name):
            results.append(str(index))
    #内测阶段,不删除文件
    # remove_pic(dir_address,img_name)
    Log.w('结果集是：'+','.join(results))
    return ','.join(results)

def remove_pic(dir_address,img_name):
    if os.path.exists(dir_address, img_name):
        os.remove(os.path.join(dir_address, img_name))

    def del_file(path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
    del_file(dir_address+'/pic')

if __name__ == '__main__':
    # cut_image('./','1.jpg')
    s1 = '你好'
    s2 = '滚蛋你妹'
    magic_char = set(s1)
    poppins_chars = set(s2)
    print(magic_char.intersection(poppins_chars))
    print(poppins_chars.intersection(magic_char))
    if magic_char.intersection(poppins_chars):
        print('yes')
    app = ['1','2','3']
    print(','.join(app))
