from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('post/show/<int:pk>/', views.show_post, name="show_post"),
    path('post/publish/<int:pk>/<slug:code>/', views.post_publish, name='post_publish'),
    path('post/delete/<int:pk>/<slug:code>', views.post_delete, name='post_delete'),
    path('post/add', views.add_post, name="add_post"),
    path('post/success/<int:pk>/', views.post_success, name="post_success"),
    url(r'^country-autocomplete/$', views.CountryAutocomplete.as_view(), name='country-autocomplete'),
    url(r'^region-autocomplete/$', views.RegionAutocomplete.as_view(), name='region-autocomplete'),
]