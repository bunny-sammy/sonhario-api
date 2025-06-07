from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

def docs_page(request):
    return render(request, 'docs.html')