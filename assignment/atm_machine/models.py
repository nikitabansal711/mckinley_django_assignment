from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, null=False, unique=True)
    email = models.EmailField(null=False)

    def __str__(self):
        return self.username


class BankAccount(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)  # Assuming one account / user
    card_number = models.CharField(max_length=8, unique=True)
    pin_number = models.CharField(max_length=4, unique=True)  # will be encrypted using cryptography library
    balance = models.BigIntegerField()

    def __str__(self):
        return self.card_number


class AtmMachine(models.Model):
    balance = models.BigIntegerField()
    ATM_2000_DENOMINATION = models.IntegerField()
    ATM_500_DENOMINATION = models.IntegerField()
    ATM_100_DENOMINATION = models.IntegerField()
