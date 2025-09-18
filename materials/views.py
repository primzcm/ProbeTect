from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import MaterialUploadForm


class MaterialUploadView(LoginRequiredMixin, View):
    template_name = "materials/upload.html"
    form_class = MaterialUploadForm

    def get(self, request):
        form = self.form_class()
        materials = request.user.materials.all()[:10]
        return render(request, self.template_name, {"form": form, "materials": materials})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        materials = request.user.materials.all()[:10]
        if form.is_valid():
            material = form.save(commit=False)
            material.owner = request.user
            material.original_filename = request.FILES['pdf'].name
            material.save()
            messages.success(request, "PDF uploaded. We will start processing it shortly.")
            return redirect("materials:upload")
        messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form, "materials": materials})
