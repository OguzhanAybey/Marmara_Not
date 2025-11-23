from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Department, Course, Note, Faculty
from .forms import NoteUploadForm


# ANASAYFA – sol tarafta fakülte/bölüm listesi + hero
def home(request):
    departments = Department.objects.all().order_by("name")
    return render(request, "notes/home.html", {
        "departments": departments,
    })


# FAKÜLTELER SAYFASI – Fakülte listesi (Kartlar)
def department_list(request):
    faculties = Faculty.objects.all().order_by("name")

    # İkon eşleştirmesi
    icon_map = {
        "Mühendislik Fakültesi": "fa-cogs",
        "İktisat Fakültesi": "fa-chart-line",
        "Hukuk Fakültesi": "fa-gavel",
        "Tıp Fakültesi": "fa-user-md",
        "Eğitim Fakültesi": "fa-book",
        "Sanat ve Tasarım Fakültesi": "fa-palette",
        "Fen-Edebiyat Fakültesi": "fa-flask",
        "İletişim Fakültesi": "fa-broadcast-tower",
        "Diş Hekimliği Fakültesi": "fa-tooth",
        "Eczacılık Fakültesi": "fa-pills",
        "İlahiyat Fakültesi": "fa-book-open",
        "Spor Bilimleri Fakültesi": "fa-running",
        "Sağlık Bilimleri Fakültesi": "fa-heartbeat",
        "Teknoloji Fakültesi": "fa-microchip",
        "İşletme Fakültesi": "fa-briefcase",
        "Siyasal Bilgiler Fakültesi": "fa-landmark",
    }

    for faculty in faculties:
        faculty.icon = icon_map.get(faculty.name, "fa-university")  # Varsayılan ikon

    return render(request, "notes/faculties.html", {
        "faculties": faculties,
    })


# FAKÜLTE DETAY – Fakülteye ait bölümler
def faculty_detail(request, slug):
    faculty = get_object_or_404(Faculty, slug=slug)
    departments = Department.objects.filter(faculty=faculty).select_related('faculty').order_by("name")
    
    # Fakülteye ait tüm dersleri getir (bölümler üzerinden)
    courses = Course.objects.filter(department__faculty=faculty).select_related('department').order_by("name")[:9] # İlk 9 dersi gösterelim
    
    return render(request, "notes/faculty_detail.html", {
        "faculty": faculty,
        "departments": departments,
        "courses": courses,
    })


# DERSLER SAYFASI – tüm dersler baloncuk olarak
def course_list(request):
    courses = Course.objects.select_related('department', 'department__faculty').all().order_by("name")
    return render(request, "notes/courses.html", {
        "courses": courses,
    })


# FAKÜLTE / BÖLÜM DETAY – seçilen fakültenin dersleri
def department_detail(request, slug):
    from django.core.paginator import Paginator
    
    department = get_object_or_404(Department.objects.select_related('faculty'), slug=slug)
    courses_list = Course.objects.filter(department=department).select_related('department').order_by("name")
    
    # Pagination - 30 courses per page
    paginator = Paginator(courses_list, 30)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    
    return render(request, "notes/department_detail.html", {
        "department": department,
        "courses": courses,
        "page_obj": courses,
    })


# DERS DETAY – dersin onaylı notları
def course_detail(request, faculty_slug, dept_slug, course_code):
    from django.core.paginator import Paginator
    
    # Fakülte ve bölüme göre dersi bul
    course = get_object_or_404(
        Course.objects.select_related('department', 'department__faculty'),
        code=course_code,
        department__slug=dept_slug,
        department__faculty__slug=faculty_slug
    )
    notes_list = Note.objects.filter(course=course, status="approved").select_related('uploader', 'course').order_by('-created_at')
    
    # Pagination - 20 not per page
    paginator = Paginator(notes_list, 20)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    return render(request, "notes/course_detail.html", {
        "department": course.department,
        "course": course,
        "notes": notes,
        "page_obj": notes,
    })


# NOT DETAY SAYFASI
def note_detail(request, note_id):
    note = get_object_or_404(Note.objects.select_related('course', 'course__department', 'uploader'), id=note_id)
    return render(request, "notes/note_detail.html", {
        "note": note,
    })


# ARAMA SAYFASI
def search(request):
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    faculties = []
    departments = []
    courses = []
    
    if query:
        # Fakülte araması
        faculties = Faculty.objects.filter(
            Q(name__icontains=query)
        ).distinct()[:5]
        
        # Bölüm araması
        departments = Department.objects.filter(
            Q(name__icontains=query)
        ).select_related('faculty').distinct()[:10]
        
        # Ders araması
        courses = Course.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        ).select_related('department', 'department__faculty').distinct()[:20]
    
    return render(request, "notes/search_results.html", {
        "query": query,
        "faculties": faculties,
        "departments": departments,
        "courses": courses,
        "total_results": len(faculties) + len(departments) + len(courses),
    })


# NOT YÜKLEME SAYFASI
@login_required
def upload_note(request):
    if request.method == "POST":
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploader = request.user
            note.status = "pending"
            note.save()

            messages.success(request, "Notun admin onayına gönderildi.")
            return redirect("home")
    else:
        form = NoteUploadForm()

    return render(request, "notes/upload_note.html", {
        "form": form,
    })


# KULLANICI NOTLARI – Kullanıcının yüklediği notlar
@login_required
def my_notes(request):
    notes = Note.objects.filter(uploader=request.user).order_by("-created_at")
    return render(request, "notes/my_notes.html", {
        "notes": notes,
    })
