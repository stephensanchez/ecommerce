# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_payment_processor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_processor',
        ),
    ]
