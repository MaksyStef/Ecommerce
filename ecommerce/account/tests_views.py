from django.test import TestCase, Client
from django.urls import reverse
from .models import Account as User



class SignViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_authenticated_user_redirects_to_homepage(self):
        user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.com')
        self.client.force_login(user)
        response = self.client.get(reverse('account:sign'))
        self.assertRedirects(response, reverse('account:settings'))

    def test_get_with_next_link_sets_session_variable(self):
        response = self.client.get(reverse('account:sign') + '?next=/some/path/')
        self.assertEqual(self.client.session['next_link'], '/some/path/')


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_view_logs_out_user_and_redirects(self):
        user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.com')
        self.client.force_login(user)
        response = self.client.get(reverse('account:logout'))
        self.assertRedirects(response, reverse('store:homepage'))
        self.assertFalse('_auth_user_id' in self.client.session)