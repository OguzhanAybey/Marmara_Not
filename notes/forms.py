from django import forms
from django.core.exceptions import ValidationError
from .models import Note
import os


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['course', 'title', 'description', 'file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if not file:
            raise ValidationError("Dosya yüklenmedi.")
        
        # 1. Dosya boyutu kontrolü (10MB)
        max_size = 10 * 1024 * 1024
        if file.size > max_size:
            raise ValidationError("Dosya boyutu 10MB'dan büyük olamaz.")
        
        # 2. Dosya uzantısı kontrolü
        ext = os.path.splitext(file.name)[1].lower()
        if ext != '.pdf':
            raise ValidationError("Sadece PDF dosyaları yükleyebilirsiniz.")
        
        # 3. PDF magic number kontrolü
        file.seek(0)
        file_start = file.read(2048)
        file.seek(0)
        
        if not file_start.startswith(b'%PDF'):
            raise ValidationError("Dosya içeriği PDF formatında değil.")
        
        # 4. Dosya adı sanitizasyonu
        dangerous_chars = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
        for char in dangerous_chars:
            if char in file.name:
                raise ValidationError("Dosya adı geçersiz karakterler içeriyor.")
        
        return file
