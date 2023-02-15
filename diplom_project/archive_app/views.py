from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "auth.html")

def auth(request):
    login = request.POST.get("username", "Undefined")
    password = request.POST.get("password", "Undefined")
    return HttpResponse(f"<h2>Login: {login} Password: {password}</h2>")