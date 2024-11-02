# Generated by Django 4.2.16 on 2024-11-02 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Koma', '0002_tickethistory_delete_changehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffectedMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SKRIPT', 'Skript'), ('TUTORIEN', 'Tutorien'), ('BOOKS', 'Bücher'), ('GENERAL', 'Allgemein')], max_length=20, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={},
        ),
        migrations.AddField(
            model_name='ticket',
            name='category',
            field=models.CharField(blank=True, choices=[('TYPO', 'Tippfehler'), ('CONTENT', 'Inhaltliche Unstimmigkeit'), ('SUGGESTION', 'Verbesserungsvorschlag'), ('GENERAL', 'Allgemein')], max_length=20, null=True, verbose_name='Kategorie'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='affected_materials',
            field=models.ManyToManyField(to='Koma.affectedmaterial', verbose_name='Betroffene Materialien'),
        ),
    ]
