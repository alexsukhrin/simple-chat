from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Message, Thread
from chat.serializers import MessageSerializer, ThreadSerializer


class ThreadCreateView(APIView):
    def post(self, request, *args, **kwargs):
        participants = request.data.get("participants")
        if len(participants) != 2:
            return Response(
                {"error": "A thread must have exactly 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants_users = User.objects.filter(id__in=participants)
        if len(participants_users) != 2:
            return Response(
                {"error": "Users not found."}, status=status.HTTP_404_NOT_FOUND
            )

        thread = Thread.objects.filter(participants__in=participants_users).distinct()
        if thread.exists():
            return Response(ThreadSerializer(thread.first()).data)

        thread = Thread.objects.create()
        thread.participants.set(participants_users)

        return Response(ThreadSerializer(thread).data)


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.filter(participants=self.request.user)


class ThreadDeleteView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread = get_object_or_404(Thread, id=self.kwargs["thread_id"])
        return Message.objects.filter(thread=thread)


class MessageMarkReadView(APIView):
    def post(self, request, *args, **kwargs):
        message = get_object_or_404(Message, id=self.kwargs["message_id"])
        if message.thread.participants.filter(id=request.user.id).exists():
            message.is_read = True
            message.save()
            return Response({"status": "marked as read"})
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)


class UnreadMessageCountView(APIView):
    def get(self, request, *args, **kwargs):
        unread_count = Message.objects.filter(thread__participants=request.user, is_read=False).count()
        return Response({"unread_count": unread_count})
