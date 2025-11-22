from django.urls import path
from . import views

urlpatterns = [
    # Ana Sayfa
    path('', views.home, name='home'),

    # Fakülteler (Bölümler) sayfası – 21 baloncuk burada listelenecek
    path('fakulteler/', views.department_list, name='department_list'),

    # DERSLER listesi (tüm ders baloncukları)
    path('dersler/', views.course_list, name='course_list'),

    # Bölüm detay (bölüme tıklayınca derslerin listesi görünür)
    path('bolum/<slug:slug>/', views.department_detail, name='department_detail'),

    # Ders detay (seçilen ders -> notlar listesi)
    path(
        'bolum/<slug:dept_slug>/ders/<slug:course_slug>/',
        views.course_detail,
        name='course_detail'
    ),

    # Not yükleme
    path('not-yukle/', views.upload_note, name='upload_note'),

    # Kullanıcı Notları
    path('notlarim/', views.my_notes, name='my_notes'),
]
