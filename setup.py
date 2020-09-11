#!/usr/bin/env python

from setuptools import setup


setup(
	name="django-push-notifications",
	packages=[
		"push_notifications",
		"push_notifications/api",
		"push_notifications/apns",
		"push_notifications/migrations",
		"push_notifications/management",
		"push_notifications/management/commands",
	],
	classifiers=CLASSIFIERS,
	description="Send push notifications to mobile devices through GCM or APNS in Django.",
	download_url="https://github.com/jleclanche/django-push-notifications/tarball/master",
	long_description=README,
	url="https://github.com/jleclanche/django-push-notifications",
	install_requires=[
		'gobiko.apns',
	],
)
