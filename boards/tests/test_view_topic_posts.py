from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Post, Topic
from ..views import PostListView

class TopicPostTests(TestCase):
  def setUp(self):
    board = Board.objects.create(name='Django', description='Django board')
    user = User.objects.create_user(username='john', email='jairus@email.com', password='123abc')
    topic = Topic.objects.create(subject='Hiyah', board=board, starter=user)
    Post.objects.create(message='mensahe ng django', topic=topic, created_by=user)
    url = reverse('topic_posts', kwargs={'pk':board.pk, 'topic_pk': topic.pk})
    self.response = self.client.get(url)

  def test_status_code(self):
    self.assertEquals(self.response.status_code, 200)

  def test_view_function(self):
    view = resolve('/boards/1/topics/1/')
    self.assertEquals(view.func.view_class, PostListView)