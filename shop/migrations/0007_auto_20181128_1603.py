# Generated by Django 2.1.3 on 2018-11-29 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20181128_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kala',
            name='pic0',
            field=models.ImageField(default='static/no-image.jpg', height_field='imageheigth', upload_to='KalaImages/20181129 - 000311', width_field='imagewidth'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic1',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 000311'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic2',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 000311'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic3',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 000311'),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='KhabarName',
            field=models.CharField(blank=True, choices=[('FALSE', 'عدم اشتراک در خبرنامه'), ('TRUE', 'مشترک خبرنامه')], default='FALSE', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='salled',
            name='sent',
            field=models.CharField(choices=[('F', 'Packege Wait for send'), ('B', 'Back to Store'), ('T', 'Packege sent')], default='F', help_text='Is package sent?', max_length=1, verbose_name='Send Status'),
        ),
    ]
