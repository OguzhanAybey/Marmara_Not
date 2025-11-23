from django.contrib import admin
from .models import Faculty, Department, Course, Note


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty', 'slug']
    list_filter = ['faculty']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'get_faculty']
    list_filter = ['department__faculty', 'department']
    search_fields = ['code', 'name', 'department__name']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_faculty(self, obj):
        return obj.department.faculty.name
    get_faculty.short_description = 'Fakülte'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'uploader', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'course__department__faculty']
    search_fields = ['title', 'course__name', 'uploader__username']
    readonly_fields = ['created_at']
    
    # Not formunda ders seçimini fakülteye göre grupla
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            # Dersleri fakülte ve bölüme göre gruplandır
            kwargs["queryset"] = Course.objects.select_related(
                'department', 'department__faculty'
            ).order_by('department__faculty__name', 'department__name', 'code')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    actions = ['approve_notes', 'reject_notes']
    
    def approve_notes(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='approved', approved_at=timezone.now())
        self.message_user(request, f'{updated} not onaylandı.')
    approve_notes.short_description = 'Seçili notları onayla'
    
    def reject_notes(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} not reddedildi.')
    reject_notes.short_description = 'Seçili notları reddet'
