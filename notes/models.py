from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Faculty(models.Model):
    """Fakülte tablosu"""
    name = models.CharField(max_length=150, verbose_name="Fakülte Adı")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Fakülte"
        verbose_name_plural = "Fakülteler"

    def __str__(self):
        return self.name


class Department(models.Model):
    """Bölüm tablosu (her bölüm bir fakülteye bağlı)"""
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name="Fakülte",
    )
    name = models.CharField(max_length=150, verbose_name="Bölüm Adı")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"

    def __str__(self):
        # Örnek çıktı: "Mühendislik Fakültesi - Bilgisayar Mühendisliği"
        return f"{self.faculty.name} - {self.name}"


class Course(models.Model):
    """Ders tablosu (her ders bir bölüme bağlı)"""
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Bölüm",
    )
    name = models.CharField(max_length=100, verbose_name="Ders Adı")
    code = models.CharField(max_length=20, blank=True, verbose_name="Ders Kodu")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Ders"
        verbose_name_plural = "Dersler"

    def __str__(self):
        dept_name = self.department.name if self.department else ""
        if self.code and dept_name:
            return f"{self.code} - {self.name} ({dept_name})"
        elif self.code:
            return f"{self.code} - {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        # slug boşsa otomatik üret
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Note(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Onay Bekliyor'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Ders",
    )
    uploader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Yükleyen Kullanıcı",
    )
    title = models.CharField(max_length=150, verbose_name="Not Başlığı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    file = models.FileField(upload_to='notes/', verbose_name="Dosya")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Durum",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Onay Tarihi")

    class Meta:
        verbose_name = "Not"
        verbose_name_plural = "Notlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
