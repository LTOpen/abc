from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction

# from decimal import Decimal, ROUND_HALF_UP

# number = Decimal('3.14159')
# rounded_number = number.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# print(rounded_number)  # 输出: 3.14


# from .tasks import process_transaction
@receiver(pre_save, sender=Transaction)
def handle_transaction_pre(sender: Transaction, instance: Transaction, **kwargs):
    try:
        previous = sender.objects.get(id=instance.id)
        instance._previous_values = {
            "from_account": previous.from_account,
            "to_account": previous.to_account,
            "amount": previous.amount,
        }

        print("Transaction changed")
    except sender.DoesNotExist:
        print("Transaction created")


@receiver(post_save, sender=Transaction)
def handle_transaction_post(sender, instance, created, **kwargs):
    if created:
        instance.from_account.balance -= instance.amount
        instance.to_account.balance += instance.amount
        instance.from_account.save()
        instance.to_account.save()
    else:
        if instance.from_account.id == instance._previous_values["from_account"].id:
            if instance.amount != instance._previous_values["amount"]:
                instance.from_account.balance += (
                    instance._previous_values["amount"] - instance.amount
                )
        else:
            instance._previous_values[
                "from_account"
            ].balance += instance._previous_values["amount"]
            instance.from_account.balance -= instance.amount
            instance._previous_values["from_account"].save()

        if instance.to_account.id == instance._previous_values["to_account"].id:
            if instance.amount != instance._previous_values["amount"]:
                instance.to_account.balance += (
                    instance.amount - instance._previous_values["amount"]
                )
        else:
            instance._previous_values[
                "to_account"
            ].balance -= instance._previous_values["amount"]
            instance.to_account.balance += instance.amount
            instance._previous_values["to_account"].save()

        instance.from_account.save()
        instance.to_account.save()
        print("Transaction changed")
