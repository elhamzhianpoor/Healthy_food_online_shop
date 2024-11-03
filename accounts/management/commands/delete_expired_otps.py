from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from accounts.models import Otp
import pytz


class Command(BaseCommand):
    help = 'Delete expired OTPs'

    def handle(self, *args, **options):
        exp_time = datetime.now() - timedelta(minutes=2)
        exp_time = exp_time.astimezone(pytz.timezone('Asia/Tehran'))

        Otp.objects.filter(created__lt=exp_time).delete()
        self.stdout.write('Successfully deleted expired OTPs')


