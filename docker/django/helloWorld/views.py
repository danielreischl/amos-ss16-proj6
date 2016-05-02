from django.shortcuts import render


def index(request):
    context = {'toGreet': 'World'}
    return render(request, 'helloWorld/index.html', context)

