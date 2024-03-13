from django.contrib import admin
from .models import Query, Resolution, QueryCategory, QueryTicket

admin.site.register(Query)
admin.site.register(QueryTicket)
admin.site.register(Resolution)
admin.site.register(QueryCategory)
