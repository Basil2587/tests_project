from django.urls import path

from . import views

urlpatterns = [
    path("group/<slug:slug>",views.group_posts),
    path("new/", views.post_new, name="new_post"),
    path("", views.index, name="index"),
        # Профайл пользователя
    path("<username>/", views.profile, name="profile"),
        # Просмотр записи
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit", views.post_edit, name="post_edit"),
    
]
