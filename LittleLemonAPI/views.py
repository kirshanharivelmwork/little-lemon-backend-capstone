from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from .permissions import is_manager, is_delivery, IsAdminOrReadOnly, IsManagerAdminOrReadOnly

def require_manager(user):
    if not is_manager(user):
        raise PermissionDenied("Manager permissions required.")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "slug"]
    ordering_fields = ["title", "slug"]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerAdminOrReadOnly]
    filterset_fields = ["category", "featured"]
    search_fields = ["title", "category__title"]
    ordering_fields = ["price", "title", "category__title"]
    ordering = ["title"]

    def perform_create(self, serializer):
        if not (self.request.user.is_staff or is_manager(self.request.user)):
            raise PermissionDenied("Only admins and managers can add menu items.")
        serializer.save()

    def perform_update(self, serializer):
        if not (self.request.user.is_staff or is_manager(self.request.user)):
            raise PermissionDenied("Only admins and managers can update menu items.")
        serializer.save()

class ManagerGroupView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        group, _ = Group.objects.get_or_create(name="Manager")
        return Response({"group": group.name, "members": list(group.user_set.values("id", "username"))})
    def post(self, request):
        username = request.data.get("username")
        if not username:
            raise ValidationError({"username": "This field is required."})
        user = get_object_or_404(User, username=username)
        group, _ = Group.objects.get_or_create(name="Manager")
        group.user_set.add(user)
        return Response({"message": f"{username} added to Manager group."}, status=status.HTTP_201_CREATED)
    def delete(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        group = Group.objects.filter(name="Manager").first()
        if group:
            group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeliveryCrewGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        require_manager(request.user)
        group, _ = Group.objects.get_or_create(name="Delivery crew")
        return Response({"group": group.name, "members": list(group.user_set.values("id", "username"))})
    def post(self, request):
        require_manager(request.user)
        username = request.data.get("username")
        if not username:
            raise ValidationError({"username": "This field is required."})
        user = get_object_or_404(User, username=username)
        group, _ = Group.objects.get_or_create(name="Delivery crew")
        group.user_set.add(user)
        return Response({"message": f"{username} added to Delivery crew."}, status=status.HTTP_201_CREATED)
    def delete(self, request):
        require_manager(request.user)
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        group = Group.objects.filter(name="Delivery crew").first()
        if group:
            group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(CartSerializer(Cart.objects.filter(user=request.user).select_related("menuitem"), many=True).data)
    def post(self, request):
        item_id = request.data.get("menuitem")
        try:
            quantity = int(request.data.get("quantity", 1))
        except (ValueError, TypeError):
            raise ValidationError({"quantity": "Enter a whole number."})
        if quantity < 1:
            raise ValidationError({"quantity": "Must be at least 1."})
        item = get_object_or_404(MenuItem, pk=item_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, menuitem=item,
            defaults={"quantity": quantity, "unit_price": item.price}
        )
        if not created:
            cart.quantity += quantity
            cart.unit_price = item.price
            cart.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = Order.objects.prefetch_related("items__menuitem").select_related("user", "delivery_crew")
        if is_manager(request.user):
            pass
        elif is_delivery(request.user):
            qs = qs.filter(delivery_crew=request.user)
        else:
            qs = qs.filter(user=request.user)
        return Response(OrderSerializer(qs, many=True).data)

    @transaction.atomic
    def post(self, request):
        cart_items = list(Cart.objects.filter(user=request.user).select_related("menuitem"))
        if not cart_items:
            raise ValidationError("Your cart is empty.")
        total = sum((row.unit_price * row.quantity for row in cart_items), Decimal("0.00"))
        order = Order.objects.create(user=request.user, total=total)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, menuitem=row.menuitem, quantity=row.quantity, unit_price=row.unit_price)
            for row in cart_items
        ])
        Cart.objects.filter(user=request.user).delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items__menuitem"), pk=pk)
        if is_manager(request.user):
            return order
        if is_delivery(request.user) and order.delivery_crew_id == request.user.id:
            return order
        if order.user_id == request.user.id:
            return order
        raise PermissionDenied("You may only access your own or assigned orders.")
    def get(self, request, pk):
        return Response(OrderSerializer(self.get_object(request, pk)).data)
    def patch(self, request, pk):
        order = self.get_object(request, pk)
        if is_delivery(request.user):
            if order.delivery_crew_id != request.user.id:
                raise PermissionDenied("This order is not assigned to you.")
            if "status" in request.data and request.data["status"] not in ["delivered", "pending"]:
                raise ValidationError({"status": "Use 'pending' or 'delivered'."})
            order.status = request.data.get("status", order.status)
        elif is_manager(request.user):
            if "delivery_crew" in request.data:
                username_or_id = request.data["delivery_crew"]
                try:
                    crew_user = User.objects.get(pk=int(username_or_id))
                except (ValueError, TypeError):
                    crew_user = get_object_or_404(User, username=username_or_id)
                if not crew_user.groups.filter(name="Delivery crew").exists():
                    raise ValidationError({"delivery_crew": "User must belong to Delivery crew group."})
                order.delivery_crew = crew_user
            if "status" in request.data:
                if request.data["status"] not in ["pending", "delivered"]:
                    raise ValidationError({"status": "Use 'pending' or 'delivered'."})
                order.status = request.data["status"]
        else:
            raise PermissionDenied("Only managers or assigned delivery crew can update orders.")
        order.save()
        return Response(OrderSerializer(order).data)

class OrderAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        require_manager(request.user)
        order = get_object_or_404(Order, pk=pk)
        crew_value = request.data.get("delivery_crew")
        if crew_value is None:
            raise ValidationError({"delivery_crew": "Provide the delivery crew user ID or username."})
        try:
            crew = User.objects.get(pk=int(crew_value))
        except (ValueError, TypeError):
            crew = get_object_or_404(User, username=crew_value)
        if not crew.groups.filter(name="Delivery crew").exists():
            raise ValidationError({"delivery_crew": "User must belong to Delivery crew group."})
        order.delivery_crew = crew
        order.save(update_fields=["delivery_crew"])
        return Response(OrderSerializer(order).data)

class ItemOfTheDayView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        item = MenuItem.objects.filter(featured=True).first()
        if not item:
            return Response({"detail": "No featured menu item has been selected."}, status=404)
        return Response(MenuItemSerializer(item).data)
    def put(self, request):
        require_manager(request.user)
        item_id = request.data.get("item_id")
        item = get_object_or_404(MenuItem, pk=item_id)
        MenuItem.objects.update(featured=False)
        item.featured = True
        item.save(update_fields=["featured"])
        return Response(MenuItemSerializer(item).data)

class HealthView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({"project": "Little Lemon API", "status": "ok"})
