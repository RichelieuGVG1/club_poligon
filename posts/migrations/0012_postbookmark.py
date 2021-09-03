# Generated by Django 3.0.4 on 2020-08-10 09:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_user_stripe_id'),
        ('posts', '0011_auto_20200523_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostBookmark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='users.User')),
            ],
            options={
                'db_table': 'post_bookmarks',
            },
        ),
    ]
