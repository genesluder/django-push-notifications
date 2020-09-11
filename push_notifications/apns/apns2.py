
from django.core.exceptions import ImproperlyConfigured

from gobiko.apns import APNsClient

from ..exceptions import NotificationError
from ..settings import PUSH_NOTIFICATIONS_SETTINGS as SETTINGS


# TODO: Common error interface for legacy and apns2
APNS_ERROR_MESSAGES = {
	1: "Processing error",
	2: "Missing device token",
	3: "Missing topic",
	4: "Missing payload",
	5: "Invalid token size",
	6: "Invalid topic size",
	7: "Invalid payload size",
	8: "Invalid token",
	10: "Shutdown",
	128: "Protocol error (APNS could not parse notification)",
	255: "Unknown APNS error",
}


class APNSError(NotificationError):
	pass


class APNSServerError(APNSError):
	def __init__(self, status, identifier):
		super(APNSServerError, self).__init__(status, identifier)
		self.status = status
		self.identifier = identifier


def _create_client():

    TEAM_ID = SETTINGS.get("APNS_TEAM_ID")
    if not TEAM_ID:
        raise ImproperlyConfigured(
            'You need to set PUSH_NOTIFICATIONS_SETTINGS["APNS_TEAM_ID"] to send messages through APNS.'
        )

    BUNDLE_ID = SETTINGS.get("APNS_BUNDLE_ID")

    APNS_AUTH_KEY_FILE = SETTINGS.get("APNS_AUTH_KEY_FILE")
    if not APNS_AUTH_KEY_FILE:
        raise ImproperlyConfigured(
            'You need to set PUSH_NOTIFICATIONS_SETTINGS["APNS_AUTH_KEY_FILE"] to send messages through APNs.'
        )

    APNS_KEY = None
    try:
        with open(APNS_AUTH_KEY_FILE, "r") as f:
            APNS_KEY = f.read()
    except Exception as e:
        raise ImproperlyConfigured("The APNs auth key file at %r is not readable: %s" % (AUTH_KEY_FILE, e))

    APNS_KEY_ID = SETTINGS.get("APNS_AUTH_KEY_ID")
    if not APNS_KEY_ID:
        raise ImproperlyConfigured(
            'You need to set PUSH_NOTIFICATIONS_SETTINGS["APNS_AUTH_KEY_ID"] to send messages through APNs.'
        )

    USE_SANDBOX = SETTINGS.get("APNS_USE_SANDBOX")

    return APNsClient(
            team_id=TEAM_ID, 
            bundle_id=BUNDLE_ID, 
            auth_key_id=APNS_KEY_ID, 
            auth_key=APNS_KEY, 
            use_sandbox=USE_SANDBOX
        )


apns_client = _create_client()


def apns_send_message(registration_id, alert, **kwargs):
    """
    Sends an APNS notification to a single registration_id.
    This will send the notification as form data.
    If sending multiple notifications, it is more efficient to use
    apns_send_bulk_message()

    Note that if set alert should always be a string. If it is not set,
    it won't be included in the notification. You will need to pass None
    to this for silent notifications.
    """

    return apns_client.send_message(registration_id, alert, **kwargs)


def apns_send_bulk_message(registration_ids, alert, **kwargs):
    """
    Sends an APNS notification to one or more registration_ids.
    The registration_ids argument needs to be a list.

    Note that if set alert should always be a string. If it is not set,
    it won't be included in the notification. You will need to pass None
    to this for silent notifications.
    """
    
    return apns_client.send_bulk_message(registration_id, alert, **kwargs)


def apns_fetch_inactive_ids(certfile=None):
    """
    Queries the APNS server for id's that are no longer active since
    the last fetch
    """
    raise Warning('The Feedback Service is no longer available. Inactive devices will be updated after a failed push notificaiton.')

