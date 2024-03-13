from django.contrib import admin
from .models import Query, Resolution, QueryCategory, QueryTicket, FollowUp

admin.site.register(Query)
admin.site.register(QueryTicket)
admin.site.register(Resolution)
admin.site.register(FollowUp)
admin.site.register(QueryCategory)
