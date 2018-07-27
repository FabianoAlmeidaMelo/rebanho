from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import Http404
from rebanho.propriedades.forms import (
    PropriedadeForm,
    PropriedadeSearchForm,
)
from rebanho.propriedades.models import Propriedade


@login_required
def propriedades_list(request):
    """
    ref #7 Listagem de propriedades
    """
    user = request.user
    
    form = PropriedadeSearchForm(request.GET or None, user=user)
    propriedades = form.get_result_queryset()
    context = {}
    can_edit = True 
    propriedades = propriedades.order_by('nome')

    # ### PAGINAÇÃO ####
    get_copy = request.GET.copy()
    context['parameters'] = get_copy.pop('page', True) and get_copy.urlencode()
    page = request.GET.get('page', 1)
    paginator = Paginator(propriedades, 15)
    try:
        propriedades = paginator.page(page)
    except PageNotAnInteger:
        propriedades = paginator.page(1)
    except EmptyPage:
        propriedades = paginator.page(paginator.num_pages)
    # ### paginação ####

    context['user'] = user
    context['form'] = form
    context['object_list'] = propriedades
    context['can_edit'] = can_edit
    context['tab_propriedades'] = "active"

    return render(request, 'propriedades/propriedades_list.html', context)


@login_required
def propriedade_form(request, pk=None):
    """
    ref #7 Cadastro e edição de Propriedades
    """
    user = request.user
    if pk:
        propriedade = get_object_or_404(Propriedade, pk=pk)
        msg = u'Propriedade alterada com sucesso. '
    else:
        propriedade = None
        msg = u'Propriedade cadastrada. '

    can_edit = True if not propriedade else propriedade.can_edit(user)
    if not can_edit:
        raise Http404

    form = PropriedadeForm(request.POST or None, instance=propriedade, user=user)
    context = {}
    context['form'] = form
    context['tab_propriedades'] = "active"

    if request.method == 'POST':
        if form.is_valid():
            propriedade = form.save()
            msg += propriedade.nome
            messages.success(request, msg)
        else:
            messages.warning(request, 'Falha no cadastro da Propriedade')
            return render(request, 'propriedades/propriedade_form.html', context)
        return redirect(reverse('propriedades_list'))
    return render(request, 'propriedades/propriedade_form.html', context)
