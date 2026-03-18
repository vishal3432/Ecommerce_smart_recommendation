from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Interaction(models.Model):
    ACTIONS = (
        ('view', 'View'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTIONS)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.action}"