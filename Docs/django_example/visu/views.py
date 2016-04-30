from django.shortcuts import render




def index(request):
    context = {'toGreet': 'out there'}
    return render(request, 'visu/index.html', context)

