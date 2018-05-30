from django.conf.urls import url
from .views import TransactionRequestView, ReturnView
from .views import SuccessTransaction


#app_name = 'transactions'

urlpatterns = [
   url(r'^completar-pago/$',
        TransactionRequestView.as_view(),
        name='complete_transaction'
    ),
   url(r'^return/$',
        ReturnView.as_view(),
        name='return_transaction'
    ),
   url(r'^return/$',
        SuccessTransaction.as_view(),
        name='success_transaction'
    ),
]
