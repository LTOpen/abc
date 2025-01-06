from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transactions"

    def ready(self):
        from .handlers import handle_transaction_post, handle_transaction_pre

        return super().ready()
