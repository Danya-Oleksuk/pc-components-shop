from django.urls import path
from api.v2.wishlists import views


app_name = "wishlists"

urlpatterns = [
    path("", views.WishlistListView.as_view(), name="wishlist-list"),
]
