from django.shortcuts import render
# API


def client(request):
    template_name = 'homepage/index.html'
    return render(request, template_name)


def list(request):
    template_name = 'homepage/index.html'
    return render(request, template_name)


def delete_client(request):
    template_name = 'homepage/index.html'
    return render(request, template_name)
