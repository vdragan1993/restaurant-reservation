from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

"""
Models for restaurant representation
"""


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    rows = models.IntegerField()
    columns = models.IntegerField()
    tables = models.IntegerField()
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Representing restaurant's menu item
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Representing restaurant's table
class Table(models.Model):
    number = models.IntegerField()
    row = models.IntegerField()
    column = models.IntegerField()
    currently_free = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.restaurant) + " " + str(self.number)


"""
Models for users representation
"""


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


# Friendship between two different users
class Friendship(models.Model):
    user = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="creator")
    friend = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="friend")
    started = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        first_person = self.user.user.get_full_name()
        second_person = self.friend.user.get_full_name()
        return first_person + " and " + second_person


"""
Models for restaurant functionality
"""


class Reservation(models.Model):
    coming = models.DateTimeField('reservation time')
    duration = models.IntegerField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        person = self.guest.user.get_full_name()
        place = self.restaurant.name
        time = self.coming
        return person + " in " + place + " at " + str(time)

    def get_finishing_time(self):
        return self.coming + datetime.timedelta(hours=self.duration)


class ReservedTables(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.reservation) + " table: " + str(self.table)


class Visit(models.Model):
    ending_time = models.DateTimeField('ending time')
    grade = models.IntegerField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.reservation) + " ending: " + str(self.ending_time) + " for: " + str(self.guest)

    def has_ended(self):
        if self.confirmed:
            return timezone.now() > self.ending_time
        else:
            return False