# Generated by Django 3.0.4 on 2020-06-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200425_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='views',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StreamView',
        ),
    ]
