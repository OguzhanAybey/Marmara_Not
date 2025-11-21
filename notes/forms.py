from django import forms
from .models import Note


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['course', 'title', 'description', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
