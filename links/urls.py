from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('<slug:username>/', UserLinks.as_view(), name='user_links'),
    path('<slug:username>/add', UserLinksCreateView.as_view(), name='add_tree'),
    path('<slug:username>/delete', UserLinksDeleteView.as_view(), name='delete_tree'),
    path('<slug:username>/<slug:tree_slug>', TreeLinks.as_view(), name='tree_links'),
    path('<slug:username>/<slug:tree_slug>/add', TreeLinksCreateView.as_view(), name='add_link'),
    path('<slug:username>/<slug:tree_slug>/delete', TreeLinksDeleteView.as_view(), name='delete_link'),
]
