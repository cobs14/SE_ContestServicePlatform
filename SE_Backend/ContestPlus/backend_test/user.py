from django.test import TestCase
from django.test.client import Client
from ContestPlus.models import User


class TestUnitOfUserRetrieve(TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建测试用数据
        User(trueName='1', username='1', password='1', emailVerifyStatus=1,
             userType='user').save()
        User(trueName='2', username='2', password='2', emailVerifyStatus=1,
             userType='user', school='清华大学').save()
        User(trueName='3', username='3', password='3', emailVerifyStatus=1,
             userType='sponsor').save()
        cls.client = Client()
        cls.cls_atomics = cls._enter_atomics()

    def setUp(self):
        self.data = {
            'params': {
                'userType': 'user',
                'username': '',
                'school': '',
                'major': '',
                'studentNumber': '',
                'getMe': 1
            },
            'pageNum': 1,
            'pageSize': 0
        }

    def tearDown(self):
        pass

    def test_sponsor_count(self):
        path = '/api/user/retrieve'
        self.data['params']['userType'] = 'sponsor'
        resp = self.client.post(path, data=self.data,
                                content_type='application/json')
        print(resp.json())
        result = resp.json()
        self.assertEqual(result['count'], 1, 'error')

    def test_user_count(self):
        path = '/api/user/retrieve'
        resp = self.client.post(path, data=self.data,
                                content_type='application/json')
        print(resp.json())
        result = resp.json()
        self.assertEqual(result['count'], 2, 'error')

    def test_school_count(self):
        path = '/api/user/retrieve'
        self.data['params']['school'] = '清华大学'
        resp = self.client.post(path, data=self.data,
                                content_type='application/json')
        print(resp.json())
        result = resp.json()
        self.assertEqual(result['data'][0]['school'], '清华大学', 'error')

    def test_username_count(self):
        path = '/api/user/retrieve'
        self.data['params']['username'] = '1'
        resp = self.client.post(path, data=self.data,
                                content_type='application/json')
        print(resp.json())
        result = resp.json()
        self.assertEqual(result['data'][0]['username'], '1', 'error')
