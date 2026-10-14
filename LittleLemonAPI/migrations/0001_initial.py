# Generated for the Little Lemon peer-review project.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Category", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("slug", models.SlugField(max_length=100, unique=True)),
            ("title", models.CharField(max_length=100)),
        ], options={"ordering": ["title"], "verbose_name_plural": "categories"}),
        migrations.CreateModel(name="MenuItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=100)),
            ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ("featured", models.BooleanField(default=False)),
            ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="menu_items", to="LittleLemonAPI.category")),
        ], options={"ordering": ["title"]}),
        migrations.CreateModel(name="Order", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("status", models.CharField(choices=[("pending", "Pending"), ("delivered", "Delivered")], default="pending", max_length=20)),
            ("total", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=8)),
            ("date", models.DateTimeField(auto_now_add=True)),
            ("delivery_crew", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_orders", to=settings.AUTH_USER_MODEL)),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-date"]}),
        migrations.CreateModel(name="Cart", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("quantity", models.PositiveSmallIntegerField(default=1)),
            ("unit_price", models.DecimalField(decimal_places=2, max_digits=6)),
            ("menuitem", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="LittleLemonAPI.menuitem")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="OrderItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("quantity", models.PositiveSmallIntegerField()),
            ("unit_price", models.DecimalField(decimal_places=2, max_digits=6)),
            ("menuitem", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="LittleLemonAPI.menuitem")),
            ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="LittleLemonAPI.order")),
        ]),
        migrations.AddConstraint(model_name="menuitem", constraint=models.CheckConstraint(condition=models.Q(("price__gte", 0)), name="menuitem_price_nonnegative")),
        migrations.AddConstraint(model_name="cart", constraint=models.UniqueConstraint(fields=("user", "menuitem"), name="unique_user_cart_item")),
    ]
