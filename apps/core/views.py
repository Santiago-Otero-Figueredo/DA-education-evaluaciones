
# Create your views here.
from django.shortcuts import redirect
from django.views import View

from apps.usuarios.models import Usuario


class Inicio(View):
    def get(self, request):

        return redirect("dashboards:inicio")

