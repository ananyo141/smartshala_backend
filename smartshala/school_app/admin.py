from django.contrib import admin

from .models import School, SchoolSection, SchoolStudent, SchoolTeacher

# Register your models here.

admin.site.register([SchoolStudent, SchoolTeacher, School])


class SchoolSectionAdmin(
    admin.ModelAdmin,
):
    list_display = ("name", "standard")


admin.site.register(SchoolSection, SchoolSectionAdmin)
