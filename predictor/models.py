from django.db import models


class QueryHistory(models.Model):
    query_text = models.TextField(max_length=255)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    predicted_outcome = models.CharField(max_length=255, default="Something gone wrong")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_text
