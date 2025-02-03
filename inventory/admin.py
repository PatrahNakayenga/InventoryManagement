from django.contrib import admin
from .models import inventoryItem,Category,Department,Staff,IssueOut
from import_export.admin import ImportExportModelAdmin



class inventoryItemAdmin(ImportExportModelAdmin):
    list_display=['name','category','quantity','issue_out_status','date_created']





admin.site.register(inventoryItem, inventoryItemAdmin)
admin.site.register(Category)

admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(IssueOut)














# Register your models here.
