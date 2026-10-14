from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, MenuItemViewSet, ManagerGroupView, DeliveryCrewGroupView,
    CartView, OrderListCreateView, OrderDetailView, OrderAssignmentView,
    ItemOfTheDayView, HealthView,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"menu-items", MenuItemViewSet, basename="menuitem")

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
    path("", include(router.urls)),
    path("groups/manager/users", ManagerGroupView.as_view(), name="manager-users"),
    path("groups/delivery-crew/users", DeliveryCrewGroupView.as_view(), name="delivery-crew-users"),
    path("cart/menu-items", CartView.as_view(), name="cart"),
    path("orders", OrderListCreateView.as_view(), name="orders"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/assign", OrderAssignmentView.as_view(), name="order-assignment"),
    path("menu-items-of-the-day", ItemOfTheDayView.as_view(), name="item-of-the-day"),
]
