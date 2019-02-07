from . import models

from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = (
            'pk', 
            'title', 
            'author', 
            'category', 
            'isbn', 
        )


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Issue
        fields = (
            'pk', 
            'shelf_id', 
            'available_status', 
        )


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Log
        fields = (
            'pk', 
            'issued_at', 
            'return_time', 
        )


