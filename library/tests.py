import unittest
from django.urls import reverse
from django.test import Client
from library.models import Book, Issue, Log
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
import datetime
import random
import string


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    username = ''.join(
        random.choice(string.ascii_lowercase) for i in range(20)
        )
    defaults["username"] = username
    defaults["email"] = "{}@tempurl.com".format(username)
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_issuer(**kwargs):
    defaults = {}
    username = ''.join(
        random.choice(string.ascii_lowercase) for i in range(20)
        )
    defaults["username"] = username
    defaults["email"] = "{}@tempurl.com".format(username)
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_book(**kwargs):
    defaults = {}
    defaults["title"] = "Computer Networking"
    defaults["author"] = "Kurose & Ross"
    defaults["category"] = "RB"
    defaults["isbn"] = "123123123"
    defaults.update(**kwargs)
    return Book.objects.create(**defaults)


def create_issue(**kwargs):
    defaults = {}
    defaults["shelf_id"] = "0001"
    defaults["available_status"] = "available"
    defaults.update(**kwargs)
    if "book" not in defaults:
        defaults["book"] = create_book()
    if "user" not in defaults:
        defaults["user"] = create_django_contrib_auth_models_user()
    return Issue.objects.create(**defaults)


def create_log(**kwargs):
    defaults = {}
    defaults["return_time"] = datetime.date(2019, 2, 10)
    defaults.update(**kwargs)
    if "book_issue" not in defaults:
        defaults["book_issue"] = create_issue()
    if "user" not in defaults:
        defaults["user"] = create_django_contrib_auth_models_user()
    if "issued_by" not in defaults:
        defaults["issued_by"] = create_django_contrib_auth_models_issuer()
    return Log.objects.create(**defaults)


class BookViewTest(unittest.TestCase):
    '''
    Tests for Book
    '''
    def setUp(self):
        self.client = Client()

    def test_list_book(self):
        url = reverse('library_book_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        url = reverse('library_book_create')
        data = {
            "title": "title",
            "author": "author",
            "category": "category",
            "isbn": "isbn",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_detail_book(self):
        book = create_book()
        url = reverse('library_book_detail', args=[book.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        book = create_book()
        data = {
            "title": "Computer Networking",
            "author": "Kurose & Ross",
            "category": "RB",
            "isbn": "123123123",
        }
        url = reverse('library_book_update', args=[book.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class IssueViewTest(unittest.TestCase):
    '''
    Tests for Issue
    '''
    def setUp(self):
        self.client = Client()

    def test_list_issue(self):
        url = reverse('library_issue_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_issue(self):
        url = reverse('library_issue_create')
        data = {
            "shelf_id": "0001",
            "available_status": "available",
            "book": create_book().pk,
            "user": create_django_contrib_auth_models_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_issue(self):
        issue = create_issue()
        url = reverse('library_issue_detail', args=[issue.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        issue = create_issue()
        data = {
            "shelf_id": "0002",
            "available_status": "issued",
            "book": create_book().pk,
            "user": create_django_contrib_auth_models_user().pk,
        }
        url = reverse('library_issue_update', args=[issue.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LogViewTest(unittest.TestCase):
    '''
    Tests for Log
    '''
    def setUp(self):
        self.client = Client()

    def test_list_log(self):
        url = reverse('library_log_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_log(self):
        url = reverse('library_log_create')
        data = {
            "return_time": datetime.date(2019, 2, 10),
            "book_issue": create_issue().pk,
            "user": create_django_contrib_auth_models_user().pk,
            "issued_by": create_django_contrib_auth_models_issuer().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_log(self):
        log = create_log()
        url = reverse('library_log_detail', args=[log.pk, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_log(self):
        log = create_log()
        data = {
            "return_time": datetime.date(2019, 2, 11),
            "book_issue": create_issue().pk,
            "user": create_django_contrib_auth_models_user().pk,
            "issued_by": create_django_contrib_auth_models_issuer().pk,
        }
        url = reverse('library_log_update', args=[log.pk, ])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
