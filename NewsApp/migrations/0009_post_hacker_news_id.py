# Generated by Django 4.2.9 on 2024-02-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0008_post_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hacker_news_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
