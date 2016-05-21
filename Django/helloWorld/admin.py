from django.contrib import admin
from .models import session
from .models import carrier
from .models import iteration
from .models import timestampdata
from .models import iterationdata

# Register your models here.
admin.site.register(session)
admin.site.register(carrier)
admin.site.register(iteration)
admin.site.register(timestampdata)
admin.site.register(iterationdata)
