from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Department, Course, Note
from .forms import NoteUploadForm


# ANASAYFA – sol tarafta fakülte/bölüm listesi + hero
def home(request):
    departments = Department.objects.all().order_by("name")
    return render(request, "notes/home.html", {
        "departments": departments,
    })


# FAKÜLTELER SAYFASI – 21 fakülte baloncuğu
def department_list(request):
    departments = Department.objects.all().order_by("name")
    return render(request, "notes/faculties.html", {
        "departments": departments,
    })


# DERSLER SAYFASI – tüm dersler baloncuk olarak
def course_list(request):
    courses = Course.objects.all().order_by("name")
    return render(request, "notes/courses.html", {
        "courses": courses,
    })


# FAKÜLTE / BÖLÜM DETAY – seçilen fakültenin dersleri
def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    courses = Course.objects.filter(department=department).order_by("name")
    return render(request, "notes/department_detail.html", {
        "department": department,
        "courses": courses,
    })


# DERS DETAY – dersin onaylı notları
def course_detail(request, dept_slug, course_slug):
    department = get_object_or_404(Department, slug=dept_slug)
    course = get_object_or_404(Course, slug=course_slug, department=department)
    notes = Note.objects.filter(course=course, status="approved")

    return render(request, "notes/course_detail.html", {
        "department": department,
        "course": course,
        "notes": notes,
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
