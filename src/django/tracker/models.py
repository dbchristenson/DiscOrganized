from django.db import models


class MemberActivity(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=100, blank=True, null=True)
    activity_name = models.CharField(max_length=100, blank=True, null=True)
    voice_channel_id = models.BigIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.username} - {self.status}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Member Activities"
