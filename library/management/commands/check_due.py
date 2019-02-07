from django.core.management.base import BaseCommand
from library.models import Log
import datetime


class Command(BaseCommand):
    help = 'Checks over due books in the database'

    def handle(self, *args, **options):
        logs = Log.objects.all()
        current_date = datetime.datetime.now().date()
        for log in logs:
            if log.return_time < current_date:
                log.status = "over_due"
                log.save()
                due_days = str(current_date - log.return_time).split(', ')[0]
            self.stdout.write(self.style.SUCCESS(
                "{} has an over due entry for {}.".format(
                    log.user.username, due_days
                    )
                )
            )
