# Generated by Django 4.2.4 on 2023-08-18 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('owner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image1', models.ImageField(upload_to='listingimages')),
                ('image2', models.ImageField(upload_to='listingimages')),
                ('image3', models.ImageField(upload_to='listingimages')),
                ('is_available', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner.owner')),
            ],
        ),
    ]