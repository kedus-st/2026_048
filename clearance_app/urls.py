from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('picture-gallery', views.picture_gallery, name='picture_gallery'),
    path('itp_edit', views.itp_edit, name='itp_edit'),
    path('visible_mtl_cols', views.visible_mtl_cols, name='visible_mtl_cols'),
    path('target-records', views.tr_view, name='tr_view'),
    path('get-sas-token/', views.get_sas_token_view, name='get_sas_token'),
    path('get-image-sources/', views.get_image_sources, name='get_image_sources'),
    path("statistics", views.statistics, name='statistics'),
    path('vessels/<int:vessel_id>/update-position/', views.update_vessel_position, name='update_vessel_position'),
]
