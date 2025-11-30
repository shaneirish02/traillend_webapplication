# ===============================================
# FINAL Scheduler Worker + Background Loop
# Works on Render Free Tier (no cron job needed)
# ===============================================

from django.utils import timezone
from firebase_admin import messaging
from core.models import Notification, DeviceToken
from core.firebase import initialize_firebase
import threading
import time

# Ensure Firebase Admin initializes only once
initialize_firebase()


def run_scheduled_notifications():
    """
    Sends all notifications whose scheduled_at time has passed.
    Called automatically by the background scheduler loop.
    """

    now = timezone.now()

    # Fetch notifications that must be sent
    due_notifications = Notification.objects.filter(
        is_sent=False,
        scheduled_at__lte=now
    ).select_related("user")

    sent_count = 0

    for notif in due_notifications:
        borrower = notif.user

        # Get device token (Expo FCM token)
        token_entry = DeviceToken.objects.filter(user=borrower).last()
        if not token_entry:
            print(f"[Scheduler] No device token for user {borrower.full_name}")
            continue

        token = token_entry.token

        try:
            # Construct FCM message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notif.title,
                    body=notif.message,
                ),
                token=token,
            )

            # Send via Firebase / FCM
            messaging.send(message)

            # Mark as sent
            notif.is_sent = True
            notif.save(update_fields=["is_sent"])

            sent_count += 1
            print(f"[Scheduler] SENT: {notif.title} → {borrower.full_name}")

        except Exception as e:
            print(f"[Scheduler][ERROR] Failed to send: {e}")

    return sent_count


# ===============================================
# BACKGROUND LOOP (run every 60 seconds)
# ===============================================

def start_scheduler_loop():
    """
    Starts a background loop that runs every 60 seconds.
    This ensures push notifications are sent even on Render free tier.
    """

    def loop():
        print("[Scheduler] Background scheduler started.")
        while True:
            try:
                run_scheduled_notifications()
            except Exception as e:
                print("[Scheduler Loop Error]", e)

            time.sleep(60)  # Run every 60 seconds

    # Daemon thread ensures it stops when Django server stops
    t = threading.Thread(target=loop, daemon=True)
    t.start()
