from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Book, Issue, Log
from .forms import BookForm, IssueForm, LogForm


class BookListView(ListView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm


class BookDetailView(DetailView):
    model = Book


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm


class IssueListView(ListView):
    model = Issue


class IssueCreateView(CreateView):
    model = Issue
    form_class = IssueForm


class IssueDetailView(DetailView):
    model = Issue


class IssueUpdateView(UpdateView):
    model = Issue
    form_class = IssueForm


class LogListView(ListView):
    model = Log


class LogCreateView(CreateView):
    model = Log
    form_class = LogForm


class LogDetailView(DetailView):
    model = Log


class LogUpdateView(UpdateView):
    model = Log
    form_class = LogForm

