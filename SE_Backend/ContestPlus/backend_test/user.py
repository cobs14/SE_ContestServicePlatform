from django.test import TestCase
from django.test.client import Client
from ContestPlus.models import User


class TestUnitOfUserRetrieve(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass
    def test_sponsor_count(self):
        path = '/api/'
        auth_data = {
            'username': self.username,
            'password': self.password
        }
        # 这里我们设置请求体格式为 json
        resp = self.client.post(path, data=auth_data,
                                content_type='application/json')
        # 将相应体转化为python 字典
        result = resp.json()
        # 检查登录结果
        self.assertEqual(result['code'], 201, result['message'])

    # 错误处理测试
    def test_function_dail(self):
        # 使用被测试的API进行一定操作，产生预期中的错误。
        # 。。。。。。
        # 检查错误处理的正确性
        # 。。。。。。
