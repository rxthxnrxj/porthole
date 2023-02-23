from django.db import models
from django.contrib.auth.models import User


class Data(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    direction = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    capture = models.ImageField(null=True, blank=True,
                                default='/placeholder.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    captureSpeed = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    capturedAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.capturedAt)


class Manual(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    left_offset = models.IntegerField(null=True, blank=True, default=0)
    right_offset = models.IntegerField(null=True, blank=True, default=0)
    width = models.IntegerField(null=True, blank=True, default=0)
    length = models.IntegerField(null=True, blank=True, default=0)
    _id = models.AutoField(primary_key=True, editable=False)
    emteredAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.enteredAt)


class Conclusion(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    v1 = models.IntegerField(null=True, blank=True, default=0)
    v2 = models.IntegerField(null=True, blank=True, default=0)
    v3 = models.IntegerField(null=True, blank=True, default=0)
    v4 = models.IntegerField(null=True, blank=True, default=0)
    v5 = models.IntegerField(null=True, blank=True, default=0)
    v6 = models.IntegerField(null=True, blank=True, default=0)
    v7 = models.IntegerField(null=True, blank=True, default=0)
    v8 = models.IntegerField(null=True, blank=True, default=0)
    v9 = models.IntegerField(null=True, blank=True, default=0)
    concludedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.concludedAt)
