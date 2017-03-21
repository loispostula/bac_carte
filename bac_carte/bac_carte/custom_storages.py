from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
import os

os.environ['S3_USE_SIGV4'] = 'True'


class S3FrankfurtStorage(S3BotoStorage):
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                settings.AWS_ACCESS_ID, settings.AWS_SECRET_ACCESS_KEY,
                calling_format=self.calling_format, host='s3.eu-central-1.amazonaws.com')
        return self._connection

class StaticStorage(S3FrankfurtStorage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3FrankfurtStorage):
    location = settings.MEDIAFILES_LOCATION
