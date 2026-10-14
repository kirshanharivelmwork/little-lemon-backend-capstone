from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, MenuItem, Cart, Order

class LittleLemonAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "AdminPass123!")
        self.customer = User.objects.create_user("customer", password="CustomerPass123!")
        self.manager_group, _ = Group.objects.get_or_create(name="Manager")
        self.manager = User.objects.create_user("manager", password="ManagerPass123!")
        self.manager.groups.add(self.manager_group)
        self.category = Category.objects.create(title="Desserts", slug="desserts")
        self.item = MenuItem.objects.create(title="Cake", price="5.00", category=self.category)

    def test_public_menu_browse(self):
        response = self.client.get("/api/menu-items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_can_add_cart_item(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post("/api/cart/menu-items", {"menuitem": self.item.id, "quantity": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.filter(user=self.customer).count(), 1)

    def test_customer_can_place_order(self):
        Cart.objects.create(user=self.customer, menuitem=self.item, quantity=2, unit_price=self.item.price)
        self.client.force_authenticate(self.customer)
        response = self.client.post("/api/orders", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(user=self.customer).count(), 1)

    def test_customer_cannot_assign_manager_group(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post("/api/groups/manager/users", {"username": "customer"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
