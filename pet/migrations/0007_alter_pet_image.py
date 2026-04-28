import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0006_alter_pet_qrid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pets/'),
        ),
    ]