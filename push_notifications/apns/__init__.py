from ..settings import PUSH_NOTIFICATIONS_SETTINGS as SETTINGS

if SETTINGS.get("APNS_VERSION") == 'APNS2':
    from .apns2 import *
else:
    from .apns_legacy import *

