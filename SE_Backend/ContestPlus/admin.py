from django.contrib import admin
from ContestPlus.backend_code.models import *

admin.site.register(User)
admin.site.register(Contest)
admin.site.register(EmailCode)
admin.site.register(Participation)
