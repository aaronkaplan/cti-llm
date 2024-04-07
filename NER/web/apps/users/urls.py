from django.urls import path

from apps.users.views import user_detail_view, user_redirect_view, user_update_view, generate_invite_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("detail/", view=user_detail_view, name="detail"),    
    path('generate-invite-code/', generate_invite_view, name='generate_invite_code'),
]
