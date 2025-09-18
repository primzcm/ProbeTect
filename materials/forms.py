from django import forms

from .models import Material

INPUT_CLASSES = "block w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-200"


class MaterialUploadForm(forms.ModelForm):
    pdf = forms.FileField(
        label="PDF",
        widget=forms.ClearableFileInput(
            attrs={"class": INPUT_CLASSES + " cursor-pointer", "accept": "application/pdf"}
        ),
        help_text="Upload a PDF up to 25 MB.",
    )

    class Meta:
        model = Material
        fields = ["title", "subject", "description", "visibility"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Material title"}),
            "subject": forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "Subject or topic"}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES, "placeholder": "Optional notes", "rows": 3}),
            "visibility": forms.Select(attrs={"class": INPUT_CLASSES}),
        }

    def clean_pdf(self):
        pdf = self.cleaned_data["pdf"]
        if pdf.size > 25 * 1024 * 1024:
            raise forms.ValidationError("Please upload a PDF smaller than 25 MB.")
        if pdf.content_type not in {"application/pdf", "application/x-pdf", "application/octet-stream"}:
            raise forms.ValidationError("Please upload a valid PDF document.")
        return pdf
