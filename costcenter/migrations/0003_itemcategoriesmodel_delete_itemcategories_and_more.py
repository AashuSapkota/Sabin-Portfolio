# Generated by Django 4.1 on 2022-08-11 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costcenter', '0002_itemcategories_alter_costcentermodel_created_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategoriesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_description', models.TextField(blank=True, null=True)),
                ('category_image', models.ImageField(null=True, upload_to='itemscategory_image')),
                ('created_by', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2022, 8, 11, 13, 53, 45, 871482))),
                ('last_updated_on', models.DateTimeField(blank=True, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ItemCategories',
        ),
        migrations.AlterField(
            model_name='costcentermodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 11, 13, 53, 45, 871482)),
        ),
    ]
