from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    return render(request, 'index.html')


def scrape(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        return render(request, 'scrape.html')
    
    return redirect('index')