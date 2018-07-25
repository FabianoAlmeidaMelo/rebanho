from django.shortcuts import render

def home(request):
    # ref #2
    # retorna o template da home
    context = {}
    return render(request, 'index.html', context)
