# Generated by Django 2.2.6 on 2021-03-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0007_auto_20210304_0902"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.CharField(
                help_text="Создайте здесь свой пост", max_length=100
            ),
        ),
    ]
