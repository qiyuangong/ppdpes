from django.contrib import admin
from .models import Anon_Task, Anon_Model, Anon_Algorithm, Data, Anon_Result, Eval_Result
# Register your models here.

# class Anon_TaskAdmin(admin.ModelAdmin):
#     fields = []


admin.site.register(Data)
admin.site.register(Anon_Model)
admin.site.register(Anon_Algorithm)
admin.site.register(Anon_Task)
admin.site.register(Anon_Result)
admin.site.register(Eval_Result)