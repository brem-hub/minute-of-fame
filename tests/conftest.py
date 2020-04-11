import pytest
from django.contrib.auth.models import User


@pytest.fixture
@pytest.mark.django_db
def login(client):
    user = User.objects.create_user('user1', 'user@user.com', 'test')
    client.login(username='user1', password='test')
    user1 = User.objects.create_user('user2', 'user@user.com', 'test')
    client.login(username='user2', password='test')
    return user, user1