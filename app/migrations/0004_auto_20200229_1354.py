# Generated by Django 3.0.3 on 2020-02-29 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_auto_20200221_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll_result', models.IntegerField()),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='badass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='badass_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_id', to=settings.AUTH_USER_MODEL),
        ),
    ]