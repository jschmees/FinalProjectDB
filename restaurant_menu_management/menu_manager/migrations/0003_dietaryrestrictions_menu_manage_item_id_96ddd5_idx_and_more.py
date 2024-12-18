# Generated by Django 5.1.3 on 2024-11-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0002_alter_restaurant_contact_number'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='dietaryrestrictions',
            index=models.Index(fields=['item'], name='menu_manage_item_id_96ddd5_idx'),
        ),
        migrations.AddIndex(
            model_name='dietaryrestrictions',
            index=models.Index(fields=['restriction_type'], name='menu_manage_restric_362a12_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['restaurant'], name='menu_manage_restaur_e052ae_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['created_date'], name='menu_manage_created_315edf_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['status'], name='menu_manage_status_23c00b_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['section'], name='menu_manage_section_3e45c8_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['item_name'], name='menu_manage_item_na_f5d1f3_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['price'], name='menu_manage_price_226238_idx'),
        ),
        migrations.AddIndex(
            model_name='menuitem',
            index=models.Index(fields=['availability_status'], name='menu_manage_availab_d705b8_idx'),
        ),
        migrations.AddIndex(
            model_name='menusection',
            index=models.Index(fields=['menu'], name='menu_manage_menu_id_89c207_idx'),
        ),
        migrations.AddIndex(
            model_name='menusection',
            index=models.Index(fields=['section_name'], name='menu_manage_section_ca9c34_idx'),
        ),
        migrations.AddIndex(
            model_name='processinglogs',
            index=models.Index(fields=['menu'], name='menu_manage_menu_id_07b940_idx'),
        ),
        migrations.AddIndex(
            model_name='processinglogs',
            index=models.Index(fields=['timestamp'], name='menu_manage_timesta_68b04a_idx'),
        ),
        migrations.AddIndex(
            model_name='processinglogs',
            index=models.Index(fields=['status'], name='menu_manage_status_e26c07_idx'),
        ),
        migrations.AddIndex(
            model_name='restaurant',
            index=models.Index(fields=['name'], name='menu_manage_name_2e9aa5_idx'),
        ),
        migrations.AddIndex(
            model_name='restaurant',
            index=models.Index(fields=['location'], name='menu_manage_locatio_37dac4_idx'),
        ),
        migrations.AddIndex(
            model_name='restaurant',
            index=models.Index(fields=['email'], name='menu_manage_email_ae4ae1_idx'),
        ),
    ]
