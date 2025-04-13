# Generated by Django 5.1.7 on 2025-04-13 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original/%Y/%m/%d/', verbose_name='Original Image')),
                ('processed_image', models.ImageField(blank=True, null=True, upload_to='processed/%Y/%m/%d/', verbose_name='Processed Image')),
                ('filters_applied', models.CharField(max_length=255, verbose_name='Applied Filters')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name': 'Processed Image',
                'verbose_name_plural': 'Processed Images',
                'ordering': ['-created_at'],
            },
        ),
    ]
