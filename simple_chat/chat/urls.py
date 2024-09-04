from django.urls import path

from .views import (MessageCreateView, MessageListView, MessageMarkReadView,
                    ThreadCreateView, ThreadDeleteView, ThreadListView,
                    UnreadMessageCountView)

urlpatterns = [
    path("threads/", ThreadCreateView.as_view(), name="thread-create"),
    path("threads/<int:pk>/", ThreadDeleteView.as_view(), name="thread-delete"),
    path("threads/list/", ThreadListView.as_view(), name="thread-list"),
    path("threads/<int:thread_id>/messages/", MessageListView.as_view(), name="message-list",),
    path("messages/", MessageCreateView.as_view(), name="message-create"),
    path("messages/<int:message_id>/read/", MessageMarkReadView.as_view(), name="message-mark-read",),
    path("messages/unread_count/", UnreadMessageCountView.as_view(), name="unread-count"),
]
