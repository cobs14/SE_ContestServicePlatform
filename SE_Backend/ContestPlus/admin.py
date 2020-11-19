from django.contrib import admin
from .models import User, Sponsor, EmailCode, Contest

admin.site.register(User)
admin.site.register(Sponsor)
admin.site.register(Contest)
admin.site.register(EmailCode)
