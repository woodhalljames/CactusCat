from django.urls import path

from .views import (
    accept_invite_view,
    remove_team_member_view,
    revoke_invite_view,
    send_invite_view,
    update_business_info_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~business-info/", view=update_business_info_view, name="update_business_info"),
    path("~invite/send/", view=send_invite_view, name="send_invite"),
    path("~invite/<int:invite_id>/revoke/", view=revoke_invite_view, name="revoke_invite"),
    path("~invite/<int:invite_id>/remove/", view=remove_team_member_view, name="remove_team_member"),
    path("invite/accept/<uuid:token>/", view=accept_invite_view, name="accept_invite"),
]
