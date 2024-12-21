from django.shortcuts import render

# Create your views here.
def render_users(request):
    return render(request,'users.html')