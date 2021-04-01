from django.shortcuts import render


def index(request):
    return render(request, "hf_public/index.html", {})

