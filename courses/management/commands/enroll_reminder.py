import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone


class Command(BaseCommand):
    help = 'Sends an e-mail reminder to users registered more than N days ago who are not enrolled in any courses.'

    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int, default=20)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a course'
        date = timezone.now() - datetime.timedelta(days=options['days'])
        users = User.objects.annotate(
            course_count=Count('courses_joined')
        ).filter(course_count=0, date_joined__date__lte=date)

        for user in users:
            message = (
                f"Dear {user.first_name or user.username},\n\n"
                "We noticed that you have not enrolled in any courses yet. "
                "Explore our courses and start learning today!"
            )
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@elearn.com')
            if user.email:
                emails.append((subject, message, from_email, [user.email]))

        if emails:
            send_mass_mail(emails)
            self.stdout.write(self.style.SUCCESS(f'Successfully sent {len(emails)} reminder email(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('No users found matching the reminder criteria.'))
