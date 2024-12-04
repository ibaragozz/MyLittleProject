from django.db import models

class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')
    created_at = models.DateTimeField(auto_now_add=True)  # Поле для времени создания

    def __str__(self):
        return self.name
