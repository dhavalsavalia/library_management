from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Book, Issue, Log
from users.models import User
from .forms import BookForm, IssueForm, LogForm
from django.shortcuts import render
from django.http import HttpResponse
from .utils import has_due
import datetime


def index(request):
    total_books = Book.objects.all().count()
    total_issues = Issue.objects.all().count()
    pending_stats = Log.objects.pending_books().count()
    due_stats = Log.objects.due_books().count()
    context = {
        'total_books': total_books,
        'total_issues': total_issues,
        'pending_stats': pending_stats,
        'due_stats': due_stats

    }
    return render(request, 'library/index.html', context)


def log_book(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            book_issue = Issue.objects.get(
                        pk=request.POST.get('book_issue_pk')
                    )
            if not has_due(request.POST.get('enrolment_number'))[0] and (book_issue.available_status == 'available'):
                issue_days = int(request.POST.get('issue_days'))
                log = Log.objects.create(
                    book_issue=Issue.objects.get(
                        pk=request.POST.get('book_issue_pk')
                    ),
                    user=User.objects.get(
                        enrolment_number=request.POST.get('enrolment_number')
                    ),
                    issued_by=request.user,
                    return_time=datetime.datetime.now().date() + datetime.timedelta(days=issue_days)
                )
                
                book_issue.available_status = "issued"
                book_issue.save()
                context = {}
                return render(request, 'library/log_book_success.html', context)
            else:
                due_books = has_due(request.POST.get('enrolment_number'))
                if due_books[0]:
                    context = {
                        'message': 'Please return due books',
                        'due_books': due_books[1]
                    }
                    return render(request, 'library/log_book_form.html', context)
                elif(book_issue.available_status != 'available'):
                    context = {
                        'message': 'Book not available'
                    }
                    return render(request, 'library/log_book_form.html', context)
        else:
            context = {
                'issues': Issue.objects.filter(available_status='available')
            }
            return render(request, 'library/log_book_form.html', context)
    else:
        return HttpResponse("Not Logged in!")


def return_book(request):
    if request.method == "POST":
        enrolment_number = request.POST.get('enrolment_number')
        issued_books = set(Log.objects.by_user(enrolment_number))
        pending_issued_books = set(Log.objects.pending_books())
        actual_issued_books = issued_books.intersection(pending_issued_books)
        due_books = has_due(enrolment_number)[1]
        context = {
            'issued_books': list(actual_issued_books),
            'due_books': due_books
        }
        return render(request, 'library/return_book_form.html', context)
    else:
        context = {}
        return render(request, 'library/return_book_form.html', context)


def return_book_handler(request):
    if request.method == 'POST':
        issued_book_pk = request.POST.get('issued_book_pk')
        issued_book = Log.objects.get(pk=issued_book_pk)
        issued_book.status = "returned"
        issued_book.save()
        issue = Issue.objects.get(pk=issued_book.book_issue.pk)
        issue.available_status = "available"
        issue.save()

        context = {
            'issued_book': Log.objects.get(pk=issued_book_pk),
            'issue': Issue.objects.get(pk=issued_book.book_issue.pk)
        }
        return render(request, 'library/return_book_handler.html', context)
    else:
        return HttpResponse(status=404)



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

