from django.urls import path
from . import views
from .views import MenuListView, MenuCreateView, OptionCreateView, MenuUpdateView, OrderCreateView, OrderListView, OrderUserList

urlpatterns = [
    path("", MenuListView.as_view(), name="menu_list"),
    path("create-menu/", MenuCreateView.as_view(), name="menu_create"),
    path("update-menu/<int:pk>/", MenuUpdateView.as_view(), name="menu_update"),
    path("create-option/", OptionCreateView.as_view(), name="option_create"),
    path("slack-send/<int:menu_id>", views.slack_send, name="slack_send"),
    path("menu/<uuid:menu_uuid>", OrderCreateView.as_view(), name="create_order"),
    path("orders-menu/<int:menu_id>", OrderListView.as_view(), name="orders_menu"),
    path("my-orders", OrderUserList.as_view(), name="my_orders")
]