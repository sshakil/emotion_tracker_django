from django.shortcuts import render

# This will serve the index.html, which loads React
def index(request):
    return render(request, 'index.html')