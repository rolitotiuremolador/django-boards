from django.test import TestCase
from django.urls import resolve, reverse
from accounts.views import signup_views
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.forms import SignUpForm

# Create your tests here.
class SignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        # url = reverse('signup')
        # response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup_views)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username' : 'keira',
            'email' : 'keira@email.com',
            'password1' : 'IbaIba42434',
            'password2' : 'IbaIba42434',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
        
    def test_redirection(self):
        '''A valid form submission should redirect the user to the home page'''
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''Create a new request to anb arbitrary page. The resulting response
        should now have a `user` to its context, after a successful sign up.'''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
    
class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {}) # submit an empty dictionary

    def test_signup_status_code(self):
        '''An invalid from submision should return to the same page'''
        self.assertEquals(self.response.status_code, 200)

    def  test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())