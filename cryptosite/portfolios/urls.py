from django.urls import path

from . import views

app_name = "portfolios"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:user_id>/", views.portfolio, name="portfolio"),
    path("<int:user_id>/add", views.add_portfolio, name="add_portfolio"),
    path("<int:user_id>/<int:portfolio_id>/add/<int:asset_id>", views.add_asset, name="add_asset"),
    path("<int:user_id>/<int:portfolio_id>/remove/<int:asset_id>", views.remove_asset, name="remove_asset"),
    path("<int:user_id>/<int:portfolio_id>/sort", views.sort_assets, name="sort_assets"),
]