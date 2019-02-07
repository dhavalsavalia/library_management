from django.contrib import admin
from django import forms
from .models import Book, Issue, Log


class BookAdminForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ['title', 'author', 'category', 'isbn']
    # readonly_fields = ['title', 'author', 'category', 'isbn']


admin.site.register(Book, BookAdmin)


class IssueAdminForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = '__all__'


class IssueAdmin(admin.ModelAdmin):
    form = IssueAdminForm
    list_display = ['shelf_id', 'available_status']
    # readonly_fields = ['shelf_id', 'available_status']


admin.site.register(Issue, IssueAdmin)


class LogAdminForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = '__all__'


class LogAdmin(admin.ModelAdmin):
    form = LogAdminForm
    list_display = ['issued_at', 'return_time']
    # readonly_fields = ['issued_at', 'return_time']


admin.site.register(Log, LogAdmin)
