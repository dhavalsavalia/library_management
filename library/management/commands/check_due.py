from django.core.management.base import BaseCommand
from library.models import Log
import datetime


class Command(BaseCommand):
    help = 'Checks over due books in the database'

    def handle(self, *args, **options):
        logs = Log.objects.all()
        current_date = datetime.datetime.now().date()
        for log in logs:
            if (log.status == "pending") and (log.return_time < current_date):
                due_days = str(current_date - log.return_time).split(', ')[0]
                log.fine = int(due_days.split(" ")[0]) * 3
                log.status = "over_due"
                log.save()

                self.stdout.write(self.style.ERROR(
                    "{} has an over due entry for {}.".format(
                        log.user.username, due_days
                        )
                    )
                )
                self.stdout.write(self.style.WARNING(
                    "\tBook: {}\n".format(
                        log.book_issue
                        )
                    ))
