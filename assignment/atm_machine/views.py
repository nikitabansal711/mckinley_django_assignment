from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, BankAccount, AtmMachine
from .serializer import UserSerializer, BankAccountSerializer, AtmMachineSerializer, AccountSerializer
from rest_framework.generics import get_object_or_404


class SignUp(APIView):
    '''
    this class consists of signup method for registring a user
    '''

    # class contain post method to register user

    def post(self, request):
        # post method to save user

        data = request.data.get("user")
        serializer = UserSerializer(data=data)
        # Serializers to check for sanity of data before using it
        if serializer.is_valid(raise_exception=True):
            atm_user = serializer.save()
            return Response('Sucessfully added user details', status=status.HTTP_200_OK)


class Register(APIView):
    '''
    this class consists of post method for registring user card details
    '''

    # class contain post method to register user card details

    def post(self, request):
        # post method to save user card details

        data = request.data.get("details")
        serializer = BankAccountSerializer(data=data)
        # Serializers to check for sanity of data before using it
        if serializer.is_valid(raise_exception=True):
            atm_user = serializer.save()
            return Response('Sucessfully added user card details ', status=status.HTTP_200_OK)


class ValidateUser(APIView):
    '''
    post method to validate user
    '''

    def post(self, request):
        data = request.data.get("details")
        # shortcut function to check user bank account else return HTTP 400 error to frontend
        user = get_object_or_404(BankAccount, card_number=data["card_number"], pin_number=data["pin_number"])
        return Response('User with {} card number exists '.format(user.card_number), status=status.HTTP_200_OK)


class Deposit(APIView):
    '''
    methos to deposi money in an user's bank account
    '''

    def put(self, request):
        data = request.data
        user_bank_detail = BankAccount.objects.get(card_number=data.get('card_number'))
        account_serializer = AccountSerializer(data=request.data, partial=True)
        if account_serializer.is_valid(raise_exception=True):
            user_bank_detail.balance = user_bank_detail.balance + data.get('deposit_amount')
            # save updated balance object
            user_bank_detail.save()
            return Response('Successfully added money to your account', status=status.HTTP_200_OK)


class Withdraw(APIView):
    '''
    method to withdraw money from a user's bank account
    '''

    def put(self, request):
        # put method to withdraw user balance on transaction, user inputs his card number, pin number and
        # withdraw_amount

        data = request.data
        account_serializer = AccountSerializer(data=request.data, partial=True)
        # Serializers to check for sanity of data before using it

        if account_serializer.is_valid(raise_exception=True):

            # get user balance object
            user_bank_detail = BankAccount.objects.get(card_number=data.get('card_number'),
                                                       pin_number=data.get('pin_number'))
            user_balance = user_bank_detail.balance

            # check if withdraw balance is greater than 20000

            if data.get('withdraw_amount') > 20000:
                return Response('Withdraw amount cannot be greater than 20000', status=status.HTTP_400_BAD_REQUEST)

            # check if user has sufficient balance or not

            if user_balance < data.get('withdraw_amount'):

                return Response('You do not have sufficient balance in your account, try with lower amount, thanks',
                                status=status.HTTP_400_BAD_REQUEST)

            else:

                # check if ATM has required balance or not which user wants to withdraw
                atm = AtmMachine.objects.get(pk=1)
                ATM_BALANCE = atm.balance
                if int(data.get('withdraw_amount')) <= ATM_BALANCE:

                    # check if user entered amount in multiples of 100, 500, 2000

                    if data.get('withdraw_amount') % 100 != 0:
                        return Response('Sorry, Mate. Please try in multiples of 100 :) ',
                                        status=status.HTTP_400_BAD_REQUEST)

                        # now reduce the denomination from ATM machine
                    else:

                        atm.ATM_2000_DENOMINATION = atm.ATM_2000_DENOMINATION - int(data.get('withdraw_amount') / 2000)
                        remain = int(data.get("withdraw_amount") % 2000)
                        if remain >= 0:
                            atm.ATM_500_DENOMINATION = int(atm.ATM_500_DENOMINATION - (remain / 500))
                            remain = remain % 500
                        if remain >= 0:
                            atm.ATM_100_DENOMINATION = int(atm.ATM_100_DENOMINATION - (remain / 100))
                            remain = remain % 100

                        user_balance = user_balance - int(data.get('withdraw_amount'))
                        user_bank_detail.balance = user_balance

                    user_bank_detail.save()

                    return Response('Thanks for your visit, please collect cash', status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response('ATM doesnt have sufficient balance, Sorry for inconvenience',
                                    status=status.HTTP_400_BAD_REQUEST)
