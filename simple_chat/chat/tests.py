from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Message, Thread


class ChatAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")
        self.user3 = User.objects.create_user(username="user3", password="pass1234")

        # Get token for authentication
        response = self.client.post(
            reverse("token_obtain_pair"), {"username": "user1", "password": "pass1234"}
        )
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a thread between user1 and user2
        self.thread = Thread.objects.create()
        self.thread.participants.set([self.user1, self.user2])
        self.thread.save()

    def tearDown(self):
        Message.objects.all().delete()
        Thread.objects.all().delete()
        User.objects.all().delete()

    def test_thread_creation(self):
        """Test thread creation"""
        response = self.client.post(
            reverse("thread-create"), {"participants": [self.user1.id, self.user3.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Thread.objects.count(), 1)

    def test_thread_creation_existing(self):
        """Test thread creation with existing participants"""
        response = self.client.post(reverse("thread-create"), {"participants": [self.user2.id, self.user3.id]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Thread.objects.count(), 1)  # No new thread should be created

    def test_thread_list(self):
        """Test retrieving thread list for a user"""
        response = self.client.get(reverse("thread-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_thread_deletion(self):
        """Test thread deletion"""
        response = self.client.delete(reverse("thread-delete", args=[self.thread.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Thread.objects.count(), 0)

    def test_message_creation(self):
        """Test message creation in a thread"""
        response = self.client.post(
            reverse("message-create"),
            {"text": "Hello, world!",
             "thread": self.thread.id,
             "sender": self.user1.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)

    def test_message_list(self):
        """Test retrieving the message list for a thread"""
        Message.objects.create(sender=self.user1, text="Hello", thread=self.thread)
        response = self.client.get(reverse("message-list", args=[self.thread.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_message_mark_as_read(self):
        """Test marking a message as read"""
        message = Message.objects.create(
            sender=self.user1, text="Hello", thread=self.thread
        )
        response = self.client.post(reverse("message-mark-read", args=[message.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertTrue(message.is_read)

    def test_unread_message_count(self):
        """Test retrieving the count of unread messages"""
        Message.objects.create(
            sender=self.user1, text="Hello", thread=self.thread, is_read=False
        )
        response = self.client.get(reverse("unread-count"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 1)
