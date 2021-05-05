from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Account
from .serializers import AccountSerializer, UserSerializer


class AccountCreatingWithTodaysSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today()
        )

    def test_create(self):
        self.assertEqual(self.account.subscription, date.today() + timedelta(settings.DEFAULT_TRIAL_PERIOD))


class AccountCreatingWithYesterdaysSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today() - timedelta(1)
        )

    def test_create(self):
        self.assertEqual(self.account.subscription, date.today() + timedelta(settings.DEFAULT_TRIAL_PERIOD))


class AccountCreatingWithTomorrowsSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today() + timedelta(1)
        )

    def test_create(self):
        self.assertEqual(self.account.subscription, date.today() + timedelta(settings.DEFAULT_TRIAL_PERIOD + 1))


class AccountWithTodaysSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today()
        )
        self.account.subscription -= timedelta(settings.DEFAULT_TRIAL_PERIOD)

    def test_set_up(self):
        self.assertEqual(self.account.subscription, date.today())

    def test_is_active(self):
        self.assertEqual(self.account.is_active(), True)

    def test_update_subscription(self):
        old_subscription = self.account.subscription
        days = 60
        self.account.update_subscription(days)
        self.assertEqual(self.account.subscription, old_subscription + timedelta(days))
        self.assertEqual(self.account.subscription, date.today() + timedelta(days))


class AccountWithYesterdaysSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today()
        )
        self.account.subscription -= timedelta(settings.DEFAULT_TRIAL_PERIOD + 1)

    def test_set_up(self):
        self.assertEqual(self.account.subscription, date.today() - timedelta(1))

    def test_is_active(self):
        self.assertEqual(self.account.is_active(), False)

    def test_update_subscription(self):
        days = 60
        self.account.update_subscription(days)
        self.assertEqual(self.account.subscription, date.today() + timedelta(days))


class AccountWithTomorrowsSubscription(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today()
        )
        self.account.subscription -= timedelta(settings.DEFAULT_TRIAL_PERIOD - 1)

    def test_set_up(self):
        self.assertEqual(self.account.subscription, date.today() + timedelta(1))

    def test_is_active(self):
        self.assertEqual(self.account.is_active(), True)

    def test_update_subscription(self):
        old_subscription = self.account.subscription
        days = 60
        self.account.update_subscription(days)
        self.assertEqual(self.account.subscription, old_subscription + timedelta(days))


class UserSerializerTests(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.serializer = UserSerializer(self.user)

    def test_password_write_only(self):
        self.assertNotEqual(self.user.password, 'password')
        self.assertEqual(set(self.serializer.data.keys()), {'id', 'username', 'email'})


class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.account = Account.objects.create(
            user=self.user,
            subscription=date.today()
        )
        self.url = reverse('account-list')

    def test_create_account(self):
        data = {
            'user': {
                'username': 'user2',
                'email': '',
                'password': 'password'
            },
            'subscription': date.today()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(
            Account.objects.get(user__username=data.get('user').get('username')).subscription,
            data.get('subscription') + timedelta(settings.DEFAULT_TRIAL_PERIOD)
        )

    def test_update_subscription(self):
        old_subscription = self.account.subscription
        days = 60
        data = {
            'id': self.account.id,
            'days': days
        }
        url = self.url + f'{self.account.id}/update_subscription/'
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Account.objects.get(id=self.account.id).subscription,
            old_subscription + timedelta(days)
        )
