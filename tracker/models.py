from django.db import models
from django.contrib.auth.models import User

class Reading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='readings')
    value = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=10, default='mg/dL')
    timestamp = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.value}{self.unit}"