from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def _split_emails(value: str):
    return [e.strip() for e in value.replace(";", ",").split(",") if e.strip()]


def _validate_multiple_emails(value: str):
    emails = _split_emails(value)
    for e in emails:
        try:
            validate_email(e)
        except ValidationError:
            raise ValidationError(f"Ungültige E-Mail-Adresse: {e}")
    return emails

class EmailActionForm(forms.Form):
    to = forms.CharField(
        label="Empfänger E-Mail(s)",
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "recipient@example.com; empfänger@beispiel.de"
        })
    )
    cc = forms.CharField(
        label="CC E-Mail(s)",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "cc1@example.com; cc2@beispiel.de"
        })
    )

    def clean_to(self):
        return _validate_multiple_emails(self.cleaned_data["to"])

    def clean_cc(self):
        value = self.cleaned_data.get("cc", "")
        return _validate_multiple_emails(value) if value else []