from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Board, Post, Topic
from ..views import PostUpdateView

class PostUpdateViewTestCase(TestCase):
  '''
  Base test case to be used in all `PostUpdateView` view test
  '''
  def setUp(self):
    self.board = Board.objects.create(name='Django', description='Django board.')
    self.username = 'keira'
    self.password = '123abd'
    user = User.objects.create_user(username=self.username, email='keira@email.com', password=self.password)
    self.topic = Topic.objects.create(subject='Hiyah!', board=self.board, starter=user)
    self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
    self.url = reverse('edit_post', kwargs={
      'pk' : self.board.pk,
      'topic_pk' : self.topic.pk,
      'post_pk' : self.post.pk
    })

class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
  def test_redirection(self):
    '''
    Test if only logged in users can edit the post
    '''
    login_url = reverse('login')
    response = self.client.get(self.url)
    self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
  def setUp(self):
    '''
    Create a new user different from the one who posted
    '''
    super().setUp()
    username = 'jairus'
    password = '321cba'
    user = User.objects.create_user(username=username, email='jairus@email.com', password=password)
    self.client.login(username=username, password=password)
    self.response = self.client.get(self.url)

  def test_status_code(self):
    '''
    A topic should be edited only by the owner.
    Unauthorized users should get a 404 response (Page Not Found)
    '''
    self.assertEquals(self.response.status_code, 404)