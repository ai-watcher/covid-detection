from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class Detection(models.Model):

    GENDERS = (('male','Male'),
              ('female','Female'),
              ('other', 'Other'),)

    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(18),
                                            MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDERS)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    image = models.ImageField(upload_to='x-rays/')
    predictions = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    def __str__(self):
        return self.fname + ' ' + self.lname
