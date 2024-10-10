from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cards/')  # Specify a folder for uploads

    def __str__(self):
        return self.title
