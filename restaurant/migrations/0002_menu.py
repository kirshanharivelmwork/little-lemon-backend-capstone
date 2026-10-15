from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("restaurant", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, unique=True)),
                ("price", models.DecimalField(max_digits=8, decimal_places=2)),
                ("inventory", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["title"]},
        ),
    ]
