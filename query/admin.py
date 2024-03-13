from django.contrib import admin
from .models import Query, Resolution, QueryCategory

admin.site.register(Query)
admin.site.register(Resolution)
admin.site.register(QueryCategory)
