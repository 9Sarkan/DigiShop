# Generated by Django 2.1.3 on 2018-11-29 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20181129_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kala',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic0',
            field=models.ImageField(default='static/no-image.jpg', height_field='imageheigth', upload_to='KalaImages/20181129 - 031905', width_field='imagewidth'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic1',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 031905'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic2',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 031905'),
        ),
        migrations.AlterField(
            model_name='kala',
            name='pic3',
            field=models.ImageField(blank=True, default='static/no-image.jpg', null=True, upload_to='KalaImages/20181129 - 031905'),
        ),
        migrations.AlterField(
            model_name='kalacat',
            name='gen',
            field=models.CharField(choices=[('f', 'female'), ('o', 'Not mind'), ('m', 'Men')], default='o', max_length=1),
        ),
        migrations.AlterField(
            model_name='myusers',
            name='KhabarName',
            field=models.CharField(blank=True, choices=[('TRUE', 'مشترک خبرنامه'), ('FALSE', 'عدم اشتراک در خبرنامه')], default='FALSE', max_length=5, null=True),
        ),
    ]
