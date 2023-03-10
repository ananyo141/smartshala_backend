from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(
    [
        models.Board,
        models.Standard,
        models.Subject,
        models.Topic,
        models.Question,
        models.Test,
    ],
)
