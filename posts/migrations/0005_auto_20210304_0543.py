# Generated by Django 2.2.6 on 2021-03-04 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_auto_20210304_0541"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(),
        ),
    ]
