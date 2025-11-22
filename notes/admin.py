from django.contrib import admin
from django.utils import timezone
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


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "uploader", "status", "created_at")
    list_filter = ("status", "course__department__faculty", "course__department")
    search_fields = ("title", "description", "course__name", "uploader__username")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    
    actions = ["approve_notes", "reject_notes"]

    @admin.action(description="Seçili notları onayla")
    def approve_notes(self, request, queryset):
        queryset.update(status="approved", approved_at=timezone.now())

    @admin.action(description="Seçili notları reddet")
    def reject_notes(self, request, queryset):
        queryset.update(status="rejected")
