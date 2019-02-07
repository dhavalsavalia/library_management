from . import models
from . import serializers
from rest_framework import viewsets, permissions


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for the Book class"""

    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for the Issue class"""

    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class LogViewSet(viewsets.ModelViewSet):
    """ViewSet for the Log class"""

    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer
    permission_classes = [permissions.IsAuthenticated]


