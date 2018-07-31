from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import Http404
from rebanho.core.forms import (
    UserForm,
    UserSearchForm,
)
from rebanho.core.models import User


def home(request):
    # ref #2
    # retorna o template da home
    context = {}
    return render(request, 'index.html', context)


@login_required
def usuarios_list(request):
    """
    ref #4 Listagem de usuários
    """
    user = request.user
    
    form = UserSearchForm(request.GET or None)
    usuarios = form.get_result_queryset().filter(id=user.id)
    context = {}
    can_edit = True 
    usuarios = usuarios.order_by('nome')

    # ### PAGINAÇÃO ####
    get_copy = request.GET.copy()
    context['parameters'] = get_copy.pop('page', True) and get_copy.urlencode()
    page = request.GET.get('page', 1)
    paginator = Paginator(usuarios, 15)
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)
    # ### paginação ####

    context['user'] = user
    context['form'] = form
    context['object_list'] = usuarios
    context['can_edit'] = can_edit
    context['tab_usuarios'] = "active"

    return render(request, 'core/usuarios_list.html', context)


@login_required
def usuario_form(request, pk=None):
    """
    ref #4 Cadastro e edição de Usuários
    """
    user = request.user
    if pk:
        usuario = get_object_or_404(User, pk=pk)
        msg = u'Usuário alterado com sucesso. '
    else:
        usuario = None
        msg = u'Usuário cadastrado. '

    can_edit = True
    if not can_edit:
        raise Http404

    form = UserForm(request.POST or None, instance=usuario, user=user)
    context = {}
    context['form'] = form
    context['tab_usuarios'] = "active"

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            msg += user.nome
            messages.success(request, msg)
        else:
            messages.warning(request, 'Falha no cadastro do Usuário')
            return render(request, 'core/usuario_form.html', context)
        return redirect(reverse('usuarios_list'))
    return render(request, 'core/usuario_form.html', context)
