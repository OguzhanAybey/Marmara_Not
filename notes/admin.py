from django.contrib import admin
from .models import Faculty, Department, Course, Note


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    list_filter = ("faculty",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "department", "get_faculty")
    list_filter = ("department__faculty", "department")
    search_fields = ("name", "code")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Fakülte")
    def get_faculty(self, obj):
        return obj.department.faculty
