from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import Http404
from rebanho.propriedades.forms import (
    AnimalForm,
    AnimalSearchForm,
    PropriedadeForm,
    PropriedadeSearchForm,
    AnimalPesagemForm,
)
from rebanho.propriedades.models import Animal, AnimalPesagem, Propriedade


def animais_list(request, propriedade_pk):
    """
    ref #8 Listagem de animais
    """
    user = request.user
    propriedade = get_object_or_404(Propriedade, pk=propriedade_pk)
    can_edit = propriedade.can_edit(user)
    if not can_edit:
        raise Http404
    pesagem = AnimalPesagem()
    form = AnimalSearchForm(request.GET or None, user=user, propriedade=propriedade)

    animais = form.get_result_queryset()
    context = {}
    context['propriedade'] = propriedade
    can_edit = True 
    animais = animais.order_by('brinco')

    # ### PAGINAÇÃO ####
    get_copy = request.GET.copy()
    context['parameters'] = get_copy.pop('page', True) and get_copy.urlencode()
    page = request.GET.get('page', 1)
    paginator = Paginator(animais, 15)
    try:
        animais = paginator.page(page)
    except PageNotAnInteger:
        animais = paginator.page(1)
    except EmptyPage:
        animais = paginator.page(paginator.num_pages)
    # ### paginação ####

    context['user'] = user
    context['form'] = form
    context['object_list'] = animais
    context['can_edit'] = can_edit
    context['menu_rebanho'] = "active"

    return render(request, 'propriedades/animais_list.html', context)


def animal_form(request, propriedade_pk, animal_pk=None):
    """
    ref #8 Cadastro e edição de animais
    """
    user = request.user
    propriedade = get_object_or_404(Propriedade, pk=propriedade_pk)

    if animal_pk:
        animal = get_object_or_404(Animal, pk=animal_pk)
        msg = u'Animal alterada com sucesso. '
    else:
        animal = None
        msg = u'Animal cadastrado. '

    can_edit = all([True if not animal else animal.can_edit(user),
                    propriedade.can_edit(user),
                    animal.propriedade.id == propriedade.id if animal else True])
    if not can_edit:
        raise Http404

    form = AnimalForm(request.POST or None, instance=animal, user=user, propriedade=propriedade)

    context = {}
    context['animal'] = animal
    context['form'] = form
    context['menu_rebanho'] = "active"
    context['propriedade'] = propriedade

    if request.method == 'POST':
        if form.is_valid():
            animal = form.save()
            msg += animal.brinco
            messages.success(request, msg)
        else:
            messages.warning(request, 'Falha no cadastro do Animal')
            return render(request, 'propriedades/animal_form.html', context)
        return redirect(reverse('animais_list', kwargs={"propriedade_pk": propriedade.id}))
    return render(request, 'propriedades/animal_form.html', context)


@login_required
def animal_pesagem_form(request, animal_pk):
    """
    ref #11 Cadastro de pesagens
    """
    user = request.user
    animal = get_object_or_404(Animal, pk=animal_pk)
    propriedade = animal.propriedade
    can_edit = animal.can_edit(user)
    if not can_edit:
        raise Http404

    msg = u'Pesagem adicionada. '
    pesagem = None
    form = AnimalPesagemForm(request.POST or None, instance=pesagem, user=user, animal=animal)

    if request.method == 'POST':
        if form.is_valid():
            pesagem = form.save()
            msg += " %s - peso: %s" % (animal.brinco, pesagem.peso)
            messages.success(request, msg)
        else:
            messages.warning(request, 'Falha no cadastro da pesagem')
            return render(request, 'propriedades/animal_pesagem_form.html', context)
        return redirect(reverse('animais_list', kwargs={"propriedade_pk": propriedade.id}))

    context = {}
    context['animal'] = animal
    context['propriedade'] = propriedade
    context['form'] = form

    return render(request, 'propriedades/animal_pesagem_form.html', context)


@login_required
def propriedades_list(request):
    """
    ref #7 Listagem de propriedades
    """
    user = request.user
    
    form = PropriedadeSearchForm(request.GET or None, user=user)
    propriedades = form.get_result_queryset()
    context = {}
    can_edit = all([propriedade.can_edit(user) for propriedade in propriedades])
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
