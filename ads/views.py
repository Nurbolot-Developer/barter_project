from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from django.contrib import messages

from . import selectors
from . import services

from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm, RegisterForm
from .serializers import AdSerializer, ExchangeProposalSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets
from rest_framework.response import Response


# --- API ViewSets для DRF ---

class AdViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ExchangeProposalViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'category', 'condition']


# --- Django views для рендеринга шаблонов ---

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'ads/ad_list.html')


def ad_list(request: HttpRequest) -> HttpResponse:
    query: Optional[str] = request.GET.get('q')
    ads = selectors.get_ads_filtered(query).order_by('-created_at')

    paginator = Paginator(ads, 10)
    page_number: Optional[str] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query or '',
    }
    return render(request, 'ads/ad_list.html', context)


def ad_detail(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = selectors.get_ad_by_id(ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def create_ad(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = services.create_ad(form.cleaned_data, request.user)
            return redirect('ads:ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def edit_ad(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = selectors.get_ad_by_id(ad_id)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = selectors.get_ad_by_id(ad_id)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == 'POST':
        ad.delete()
        return redirect('ads:ad_list')

    return render(request, 'ads/delete_ad.html', {'ad': ad})


@login_required
def propose_exchange(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = selectors.get_ad_by_id(ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.proposer = request.user
            proposal.target_ad = ad
            proposal.save()
            return redirect('ads:ad_detail', ad_id=ad.id)
    else:
        form = ExchangeProposalForm()
        form.fields['offered_ad'].queryset = selectors.get_user_ads_except(ad.id, request.user)

    return render(request, 'ads/propose_exchange.html', {'form': form, 'ad': ad})


@login_required
def create_exchange_proposal(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = selectors.get_ad_by_id(ad_id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['ad_receiver'] = ad.id
            proposal = services.create_exchange_proposal(data, request.user)
            return redirect('ads:ad_detail', ad_id=ad.id)
    else:
        user_ads = selectors.get_user_ads_except(ad.id, request.user)
        form = ExchangeProposalForm()
        form.fields['ad_sender'].queryset = user_ads

    return render(request, 'ads/create_exchange_proposal.html', {'form': form, 'ad': ad})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect("login")
        else:
            messages.error(request, "Ошибка в данных регистрации.")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})
