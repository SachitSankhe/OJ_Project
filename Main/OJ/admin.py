from django.contrib import admin

from .models import Problem, Solution, TestCase

class TestCasesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.

admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(TestCase,TestCasesAdmin)
