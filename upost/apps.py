
from django.apps import AppConfig
from django.conf import settings
from django.core.urlresolvers import get_callable
from .models import Post

class upostAppConfig(AppConfig):

    name = 'upost'
    verbose_name = 'upost'

    def ready(self):
        # Post.objects.first()
        pass
