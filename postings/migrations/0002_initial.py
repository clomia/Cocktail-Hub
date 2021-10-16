# Generated by Django 3.2.5 on 2021-10-16 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('postings', '0001_initial'),
        ('archives', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='replylike',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replylike',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to='postings.reply'),
        ),
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='postings.comment'),
        ),
        migrations.AddField(
            model_name='reply',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postinglike',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postinglike',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting_likes', to='postings.posting'),
        ),
        migrations.AddField(
            model_name='posting',
            name='constituents',
            field=models.ManyToManyField(related_name='postings', to='archives.Constituent'),
        ),
        migrations.AddField(
            model_name='posting',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posting',
            name='flavor_tags',
            field=models.ManyToManyField(related_name='postings', to='archives.FlavorTag'),
        ),
        migrations.AddField(
            model_name='picture',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='postings.posting'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='postings.comment'),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='postings.posting'),
        ),
    ]
