# Generated by Django 4.2.5 on 2023-11-18 21:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("wallet", "0007_bankaccount_save_account")]

    operations = [
        migrations.RenameField(
            model_name="transaction", old_name="payee", new_name="user"
        ),
        migrations.RemoveField(model_name="transaction", name="payor"),
    ]
