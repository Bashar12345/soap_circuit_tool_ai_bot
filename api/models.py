from django.db import models

class Conversation(models.Model):
    # user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)  
    user_id = models.CharField(max_length=100, blank=True, null=True)  # String identifier (e.g., session key or 'anonymous')
    # user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField()  # User's question
    response = models.TextField()  # AI's response
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the interaction

    class Meta:
        ordering = ['timestamp']  # Order by timestamp (oldest to newest)

    def __str__(self):
        return f"Q: {self.question[:50]}... | R: {self.response[:50]}..."