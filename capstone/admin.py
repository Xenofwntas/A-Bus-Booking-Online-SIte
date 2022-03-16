from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Route)
admin.site.register(Places)
admin.site.register(Images)
admin.site.register(Ticket)