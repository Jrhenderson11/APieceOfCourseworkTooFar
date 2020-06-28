from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.forms import CVForm
from django.contrib.auth import get_user_model

# View imports
from blog.views import *

class BlogTest(TestCase):

    User = get_user_model()

    def setUp(self):
        user = self.User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_template(self):

        self.assertTemplateUsed(self.client.get('/'), 'blog/post_list.html')
        self.assertTemplateUsed(self.client.get('/cv'), 'blog/cv.html')

    def test_cv_edit_auth(self):
        # Test edit page has authentication

        # should be redirected to cv if not authenticated
        self.assertTemplateUsed(self.client.get('/cv/edit', follow=True), 'blog/cv.html')

        self.client.login(username='temporary', password='temporary')

        self.assertTemplateUsed(self.client.get('/cv/edit', follow=True), 'blog/cv_edit.html')
        self.client.logout()

    def test_edit_button(self):
        # Test authed users can see edit button
        self.client.login(username='temporary', password='temporary')
        self.assertIn(b'/cv/edit', self.client.get('/cv', follow=True).content)
        self.client.logout()

    def test_edit_form(self):
        # Test valid and invalid forms

        form = CVForm(data={})
        self.assertFalse(form.is_valid())
        form = CVForm(data={'skills': 'new skills', 'education': 'new education'})
        self.assertTrue(form.is_valid())
