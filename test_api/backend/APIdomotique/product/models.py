from django.db import models

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    prince = models.DecimalField(max_digits=15, decimal_places=2)
    
    @property
    def get_discount(self):
        return "%.2f"%(float(self.prince) *0.5)

