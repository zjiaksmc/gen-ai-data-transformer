from django.db import models


class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=128)
    session_name = models.CharField(max_length=50)
    created_dt = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'copilot_chat_session'