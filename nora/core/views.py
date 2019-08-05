from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def createMenu(request):
    return render(request, "core/create_menu.html")

def createOption(request):
    return render(request, "core/create_option.html")