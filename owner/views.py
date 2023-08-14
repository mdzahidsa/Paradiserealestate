from django.shortcuts import render




# Create your views here.

def oprofile(request):
    return render(request, 'owner/oprofile.html')