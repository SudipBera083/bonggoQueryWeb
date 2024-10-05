from django.shortcuts import render

# Create your views here.
def colaborate(request):
    return render(request, "colaborate/index.html")