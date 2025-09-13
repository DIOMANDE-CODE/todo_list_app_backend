# Automatisation de la suppresion des tokens expirés

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


def cleanTokenExpiry():

    today = timezone.now()

    # Suppression des token expirés
    token_expired = OutstandingToken.objects.filter(expires_at__lt=today)
    count_expired = token_expired.count()
    token_expired.delete()

    # Suppression des token blacklisté expirés
    blacklisted = BlacklistedToken.objects.filter(token_expired__lt=today)
    count_blacklisted = blacklisted.count()
    blacklisted.delete()

    return f"{count_expired} tokens expirés, et {count_blacklisted} token blacklistés ont été supprimés"

def start_cleanTokenExpiry():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanTokenExpiry, 'interval', hours=1)
    scheduler.start()