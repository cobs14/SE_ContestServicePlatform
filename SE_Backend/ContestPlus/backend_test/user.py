from django.test import TestCase
from django.test.client import Client
from ContestPlus.models import User


class TestUnitOfUserRetrieve(TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = User(trueName='1',
            username='1', password='1', emailVerifyStatus=1, userType='user')
        tmp.save()
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
        resp = self.client.post(path, data=self.data,
                                content_type='application/json')
        print(resp.json())
        result = resp.json()
        self.assertEqual(result['count'], 1, 'error')
