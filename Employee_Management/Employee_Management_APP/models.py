from django.db import models


class Employee(models.Model):
    DESIGNATION_CHOICES = [
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Tester', 'Tester'),
       
    ]

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, editable=False) 
    short_description = models.TextField()

    def __str__(self):
        return self.name