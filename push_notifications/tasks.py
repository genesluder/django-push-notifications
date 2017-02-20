# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from gobiko.apns.exceptions import BadDeviceToken

from push_notifications.apns.apns2 import apns_send_message
from push_notifications.models import APNSDevice

@shared_task()
def apns_send_message_task(registration_id, message, **kwargs):
    
    try:
        response = apns_send_message(registration_id=registration_id, alert=message, **kwargs)
    except BadDeviceToken:
        device = APNSDevice.objects.get(registration_id=registration_id)
        device.active = False
        device.save()

