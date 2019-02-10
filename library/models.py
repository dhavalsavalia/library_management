from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class BookManager(models.Manager):
    def reference_books(self):
        return self.filter(category="RB")

    def text_books(self):
        return self.filter(category="TB")


class Book(models.Model):
    """Defines Book table in the database

    Attributes:
        title (str):
        author (str, optional):
        category (str):
        isbn (str, optional):

    """

    CATEGORY_CHOICES = (
        ('RB', 'Reference Book'),
        ('TB', 'Text Book')
    )

    title = models.CharField(
        max_length=50,
        blank=True, null=True
        )
    author = models.CharField(
        max_length=50,
        blank=True, null=True
        )
    category = models.CharField(
        max_length=10,
        blank=True, null=True,
        choices=CATEGORY_CHOICES
        )
    isbn = models.CharField(
        max_length=20,
        blank=True, null=True
        )

    objects = BookManager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('library_book_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('library_book_update', args=(self.pk,))


class Issue(models.Model):

    AVAILABLE_STATUS_CHOICES = (
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('lost', 'Lost')
    )

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        on_delete=models.CASCADE
        )

    shelf_id = models.CharField(
        max_length=20,
        blank=True, null=True
        )
    available_status = models.CharField(
        max_length=20,
        blank=True, null=True,
        choices=AVAILABLE_STATUS_CHOICES
        )

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")

    def __str__(self):
        return self.book.title + " " + self.shelf_id

    def __unicode__(self):
        return self.book.title + " " + self.shelf_id

    def get_absolute_url(self):
        return reverse('library_issue_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('library_issue_update', args=(self.pk,))


class LogManager(models.Manager):
    def by_user(self, enrolment_number):
        return self.filter(user__enrolment_number=enrolment_number)

    def by_issuer(self):
        return self.filter(category="TB")

    def pending_books(self):
        return self.filter(status="pending")

    def due_books(self):
        return self.filter(status="over_due")

    def issued_between(self, from_date, to_date):
        return self.filter(date__range=[from_date, to_date])


class Log(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("returned", "Returned"),
        ("over_due", "Over Due")
    )

    book_issue = models.ForeignKey(
        'Issue',
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='borrower',
        blank=True, null=True,
        on_delete=models.CASCADE
        )
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='issuer',
        blank=True, null=True,
        on_delete=models.CASCADE
        )
    issued_at = models.DateField(auto_now_add=True)
    return_time = models.DateField()
    status = models.CharField(
        max_length=20,
        blank=True, null=True,
        choices=STATUS_CHOICES,
        default="pending"
        )
    fine = models.IntegerField(
        default=0
    )
    
    objects = LogManager()

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.book_issue.shelf_id + " " + self.user.username

    def __unicode__(self):
        return self.book_issue.shelf_id + " " + self.user.username

    def get_absolute_url(self):
        return reverse('library_log_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('library_log_update', args=(self.pk,))
