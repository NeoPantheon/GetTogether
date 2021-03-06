# Generated by Django 2.0 on 2018-09-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0044_add_event_settings")]

    operations = [
        migrations.AlterField(
            model_name="commonevent",
            name="announce_url",
            field=models.URLField(
                blank=True, null=True, verbose_name="Announcement URL"
            ),
        ),
        migrations.AlterField(
            model_name="commonevent",
            name="end_time",
            field=models.DateTimeField(db_index=True, verbose_name="End Time"),
        ),
        migrations.AlterField(
            model_name="commonevent",
            name="start_time",
            field=models.DateTimeField(db_index=True, verbose_name="Start Time"),
        ),
        migrations.AlterField(
            model_name="commonevent",
            name="summary",
            field=models.TextField(
                blank=True, help_text="Markdown formatting supported", null=True
            ),
        ),
        migrations.AlterField(
            model_name="commonevent",
            name="web_url",
            field=models.URLField(blank=True, null=True, verbose_name="Website URL"),
        ),
        migrations.AlterField(
            model_name="event",
            name="announce_url",
            field=models.URLField(
                blank=True, null=True, verbose_name="Announcement URL"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="end_time",
            field=models.DateTimeField(db_index=True, verbose_name="End Time"),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_time",
            field=models.DateTimeField(db_index=True, verbose_name="Start Time"),
        ),
        migrations.AlterField(
            model_name="event",
            name="summary",
            field=models.TextField(
                blank=True, help_text="Markdown formatting supported", null=True
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="web_url",
            field=models.URLField(blank=True, null=True, verbose_name="Website URL"),
        ),
        migrations.AlterField(
            model_name="eventcomment",
            name="body",
            field=models.TextField(help_text="Markdown formatting supported"),
        ),
    ]
