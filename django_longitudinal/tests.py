from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from django_longitudinal.views import home

# Create your tests here.

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve("/")
		self.assertEqual(found.func, home)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home(request)

		self.assertTrue(response.content.startswith(b"<html>"))
		self.assertIn(b"<title>Variables</title>",response.content)
		self.assertTrue(response.content.endswith(b"</html>"))