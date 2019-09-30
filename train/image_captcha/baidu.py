import requests
from configure import BAIDU_API_KEY,BAIDU_APP_ID,BAIDU_SECRET_ID
from aip import AipImageClassify, AipOcr


class ImageClassify:
    def __init__(self,app_id,api_key,secret_key):
        self.image_client = AipImageClassify(app_id,api_key,secret_key)
        self.words_client = AipOcr(app_id,api_key,secret_key)

    def _get_token(self):
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+self.api_key+'&client_secret='+self.secret_key
        response = requests.get(url)

        if response and response.status_code == 200:
            content = response.json()
            token = content.get('access_token') or ''
            return token
        return None

    def _get_file_content(self,file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()

    def resolve_image(self,file_path):
        try:
            image = self._get_file_content(file_path)
            contents = self.image_client.advancedGeneral(image)
            result = contents.get('result')[0]
        except Exception as e:
            return ''
        return result.get('keyword')

    def resolve_words(self,file_path):

        try:
            words = self._get_file_content(file_path)
            contents = self.words_client.basicGeneral(words)
            result = contents.get('words_result')[0]
        except Exception as e:
            return ''
        return result.get('words')

if __name__ == '__main__':

    image = ImageClassify(BAIDU_APP_ID,BAIDU_API_KEY,BAIDU_SECRET_ID)
    image.resolve_words('./pic/1.png')
    image.resolve_image('./pic/1_1.png')
    image.resolve_image('./pic/1_2.png')
    image.resolve_image('./pic/1_3.png')
    image.resolve_image('./pic/1_4.png')
    image.resolve_image('./pic/1_5.png')
    image.resolve_image('./pic/1_6.png')
    image.resolve_image('./pic/1_7.png')
    image.resolve_image('./pic/1_8.png')
