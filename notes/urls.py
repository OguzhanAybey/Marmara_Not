from django.urls import path
from . import views

urlpatterns = [
    # Ana Sayfa
    path('', views.home, name='home'),

    # Fakülteler (Bölümler) sayfası – 21 baloncuk burada listelenecek
    path('fakulteler/', views.department_list, name='department_list'),

    # DERSLER listesi (tüm ders baloncukları)
    path('dersler/', views.course_list, name='course_list'),

    # Fakülte Detay (Fakülteye tıklayınca bölümlerin listesi görünür)
    path('fakulte/<slug:slug>/', views.faculty_detail, name='faculty_detail'),

    # Bölüm detay (bölüme tıklayınca derslerin listesi görünür)
    path('bolum/<slug:slug>/', views.department_detail, name='department_detail'),

    # Ders detay sayfası (faculty + department + course code ile)
    path('ders/<slug:faculty_slug>/<slug:dept_slug>/<str:course_code>/', views.course_detail, name='course_detail'),

    # Not Detay Sayfası
    path('not/<int:note_id>/', views.note_detail, name='note_detail'),

    # Arama
    path('arama/', views.search, name='search'),

    # Not yükleme
    path('not-yukle/', views.upload_note, name='upload_note'),

    # Kullanıcı Notları
    path('notlarim/', views.my_notes, name='my_notes'),
    
    # Authentication
    path('giris/', views.login_view, name='login'),
    path('kayit/', views.register_view, name='register'),
    path('cikis/', views.logout_view, name='logout'),
    
    # Password Reset
    path('sifre-sifirlama/', 
         views.password_reset_request, 
         name='password_reset'),
    path('sifre-sifirlama/gonderildi/', 
         views.password_reset_done, 
         name='password_reset_done'),
    path('sifre-sifirlama/<uidb64>/<token>/', 
         views.password_reset_confirm, 
         name='password_reset_confirm'),
    path('sifre-sifirlama/tamamlandi/', 
         views.password_reset_complete, 
         name='password_reset_complete'),
]
