from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from errorcentralapp.models import ErrorLog, AppException, Agent


class ViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='T3stP4ssw0rd'
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.create_objects()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.token))

    def create_objects(self):
        e1 = AppException.objects.create(title='NullPointerException')
        a1 = Agent.objects.create(address='http://127.0.0.1:8080/')
        ErrorLog.objects.create(description='in method save() at line 5',
                                level='ERR',
                                environment='DEV',
                                agent=a1,
                                user=self.user,
                                exception=e1)
        e2 = AppException.objects.create(title='BadRequestException')
        a2 = Agent.objects.create(address='https://www.production.com/')
        ErrorLog.objects.create(description='in method update() at line 3',
                                level='WRN',
                                environment='PRD',
                                agent=a2,
                                user=self.user,
                                exception=e2)

    def test_should_retrieve_all_log_list(self):
        response = self.client.get('/api/logs/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_should_retrieve_logs_filtered_by_environment(self):
        response = self.client.get('/api/logs/?environment=PRD')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['environment'], 'PRD')

    def test_should_retrieve_logs_filtered_by_level(self):
        response = self.client.get('/api/logs/?level=ERR')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['level'], 'ERR')

    def test_should_retrieve_logs_filtered_by_description(self):
        response = self.client.get('/api/logs/?description=update')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['description'], 'in method update() at line 3')

    def test_should_retrieve_logs_filtered_by_agent(self):
        response = self.client.get('/api/logs/?agent=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['agent']['address'], 'https://www.production.com/')

    def test_should_create_log(self):
        log = {'agent': 1,
               'environment': 'PRD',
               'level': 'ERR',
               'description': 'ErrorDescription',
               'exception': 1
               }
        response = self.client.post('/api/logs/', data=log, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], log['description'])

    def test_should_retrieve_log_by_id(self):
        response = self.client.get('/api/logs/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_should_remove_log_by_id(self):
        delete_response = self.client.delete('/api/logs/1/')
        get_response = self.client.get('/api/logs/1/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_create_log_when_environment_is_invalid(self):
        log = {'agent': 1,
               'environment': 'INVALID_ENV',
               'level': 'ERR',
               'description': 'ErrorDescription',
               'exception': 1
               }
        response = self.client.post('/api/logs/', data=log, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['environment'][0], '\"INVALID_ENV\" is not a valid choice.')

    def test_should_not_create_log_when_level_is_invalid(self):
        log = {'agent': 1,
               'environment': 'DEV',
               'level': 'INVALID_LEVEL',
               'description': 'ErrorDescription',
               'exception': 1
               }
        response = self.client.post('/api/logs/', data=log, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['level'][0], '\"INVALID_LEVEL\" is not a valid choice.')

    def test_should_retrieve_logs_filtered_by_exception(self):
        response = self.client.get('/api/logs/?exception=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)

    def test_should_retrieve_summaries(self):
        response = self.client.get('/api/summaries/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)
        self.assertEqual(response.data['results'][0]['events'], 1)

    def test_should_retrieve_summaries_filtered_by_exception(self):
        response = self.client.get('/api/summaries/?exception=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['exception']['id'], 1)
        self.assertEqual(response.data['results'][0]['events'], 1)
