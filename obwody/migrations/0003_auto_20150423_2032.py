# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obwody', '0002_auto_20150423_1831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obwód',
            old_name='carts',
            new_name='cards',
        ),
    ]
