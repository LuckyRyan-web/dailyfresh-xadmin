from django.shortcuts import render
from .models import *
from django.views.generic.base import View

# Create your views here.
class Index(View):
    def get(self,request):
        return render(request,'index.html')