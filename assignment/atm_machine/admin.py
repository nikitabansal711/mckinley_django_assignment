
from django.contrib import admin

from atm_machine.models import User, BankAccount, AtmMachine


admin.site.register(User)
admin.site.register(BankAccount)
admin.site.register(AtmMachine)


