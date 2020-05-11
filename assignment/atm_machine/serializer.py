from rest_framework import serializers

from .models import User, BankAccount, AtmMachine


class UserSerializer(serializers.ModelSerializer):
    '''
    serializer for user model
    '''
    class Meta:
        model = User
        fields = ('username', 'email')


class BankAccountSerializer(serializers.ModelSerializer):
    '''
    serializer for bank account model
    '''
    class Meta:
        model = BankAccount
        fields = ('user', 'card_number', 'pin_number', 'balance')


class AccountSerializer(serializers.ModelSerializer):
    '''
    serializer for bank account model with card number and pin number as read only fields
    '''
    class Meta:
        model = BankAccount
        fields = ('user', 'card_number', 'pin_number', 'balance')
        read_only_fields = ('card_number', 'pin_number')


class AtmMachineSerializer(serializers.ModelSerializer):
    '''
    xerializer for atm machine model
    '''
    class Meta:
        model = AtmMachine
        fields = ('balance', 'ATM_2000_DENOMINATION', 'ATM_500_DENOMINATION ', 'ATM_100_DENOMINATION')
