from django.contrib import admin
from .models import tbl_Session
from .models import tbl_Carrier
from .models import tbl_Iteration
from .models import tbl_TimeStampData
from .models import tbl_IterationData

# Register your models here.
admin.site.register(tbl_Session)
admin.site.register(tbl_Carrier)
admin.site.register(tbl_Iteration)
admin.site.register(tbl_TimeStampData)
admin.site.register(tbl_IterationData)
