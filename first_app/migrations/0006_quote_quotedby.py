# Generated by Django 2.2.4 on 2020-05-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_remove_quote_quotedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='quotedby',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
