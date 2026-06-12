from django import forms
from .models import UnlinkedImage
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class UnlinkedImageForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), 
        required=False,
        label='Upload New Images'
    )

    class Meta:
        model = UnlinkedImage
        fields = ['images', 'notes']

    def save(self, commit=True):
        images = self.files.getlist('images')
        instances = []
        for image in images:
            instance = UnlinkedImage(image=image, notes=self.cleaned_data.get('notes', ''))
            if commit:
                instance.save()
            instances.append(instance)
        return instance

    def save_m2m(self):
        self._save_m2m()
        #pass  # This method is necessary to prevent the AttributeError

class UploadFilesForm(forms.Form):
    docs = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
