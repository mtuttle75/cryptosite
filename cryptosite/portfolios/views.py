from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse
from portfolios.models import Asset, Portfolio

def index(request):
    user_list = User.objects.filter(is_superuser=False)
    context = {"user_list": user_list}
    return render(request, "portfolios/index.html", context)

def portfolio(request, user_id):
    portfolio = {}
    available_assets = {}
    portfolio_assets = {}
    portfolio_exist = Portfolio.objects.filter(user_id=user_id).exists()
    if portfolio_exist:
        portfolio = Portfolio.objects.get(user_id=user_id)
        available_assets = Asset.objects.exclude(id__in=portfolio.assets.values('id'))
        portfolio_assets = portfolio.assets.all()
    else:
        available_assets = Asset.objects.all()

    return render(request,
                  "portfolios/portfolio.html",
                  {"portfolio": portfolio, "user_id": user_id, "available_assets": available_assets, "portfolio_assets": portfolio_assets}
                 )

def add_portfolio(request, user_id):
    name = request.POST["name"]
    
    if not name or len(name) > 50:
        error_message = 'Invalid Name. Must be between 1 to 50 characters'
        return render(request, "portfolios/portfolio.html", {"portfolio": {}, "user_id": user_id, "error_message": error_message})
    
    portfolio_exist = Portfolio.objects.filter(user_id=user_id).exists()
    user_exist = User.objects.filter(id=user_id).exists()

    if not portfolio_exist and user_exist:
        user = User.objects.get(id=user_id)
        portfolio = Portfolio(name=name, user=user)
        portfolio.save()

    return HttpResponseRedirect(reverse("portfolios:portfolio", args=(user_id,)))

def add_asset(request, user_id, portfolio_id, asset_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    asset = get_object_or_404(Asset, pk=asset_id)
    is_user_portfolio = portfolio.user.pk == user_id
    has_asset = portfolio.assets.filter(id=asset_id).exists()

    if is_user_portfolio and not has_asset:
        portfolio.assets.add(asset)
        portfolio.save()

    return HttpResponseRedirect(reverse("portfolios:portfolio", args=(user_id,)))

def remove_asset(request, user_id, portfolio_id, asset_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    asset = get_object_or_404(Asset, pk=asset_id)
    is_user_portfolio = portfolio.user.pk == user_id
    has_asset = portfolio.assets.filter(id=asset_id).exists()

    if is_user_portfolio and has_asset:
        portfolio.assets.remove(asset)
        portfolio.save()

    return HttpResponseRedirect(reverse("portfolios:portfolio", args=(user_id,)))

def sort_assets(request, user_id, portfolio_id):
    clear = request.POST.get("clear", False)
    sort_by_market_cap = request.POST.get("market_cap", False)
    sort_by_daily_change = request.POST.get("change_daily", False)
    sort_by_volume = request.POST.get("volume", False)

    if clear or (not sort_by_market_cap and not sort_by_daily_change and not sort_by_volume):
        return HttpResponseRedirect(reverse("portfolios:portfolio", args=(user_id,)))

    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    is_user_portfolio = portfolio.user.pk == user_id
    portfolio_assets = {}

    if is_user_portfolio:
        portfolio_assets = _sort_portfolio_assets(portfolio, sort_by_market_cap, sort_by_daily_change, sort_by_volume)

    available_assets = Asset.objects.exclude(id__in=portfolio.assets.values('id'))
    return render(request,
                  "portfolios/portfolio.html",
                  {"portfolio": portfolio, "user_id": user_id, "available_assets": available_assets, "portfolio_assets": portfolio_assets}
                 )

def _sort_portfolio_assets(portfolio:Portfolio, sort_by_market_cap, sort_by_daily_change, sort_by_volume):
    if sort_by_market_cap:
        return portfolio.assets.all().order_by('-market_cap')
    elif sort_by_daily_change:
        return portfolio.assets.all().order_by('-change_daily')
    elif sort_by_volume:
        assets = portfolio.assets.all().order_by('-volume')
        if assets.count() > 0:
            new_list = []
            new_list.append(VolumeAsset(assets.first(), True))
            for asset in assets[1:]:
                print(asset.id)
                new_list.append(VolumeAsset(asset, False))
            return new_list
        else:
            return assets
        
    
class VolumeAsset():
    def __init__(self, asset, is_highest_volume):
        self.id = asset.id
        self.name = asset.name
        self.symbol = asset.symbol
        self.price = asset.price
        self.market_cap = asset.market_cap
        self.volume = asset.volume
        self.change_daily = asset.change_daily
        self.created_at = asset.created_at
        self.last_updated = asset.last_updated
        self.is_highest_volume = is_highest_volume