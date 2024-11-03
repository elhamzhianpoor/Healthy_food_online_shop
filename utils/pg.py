from unittest import case

import requests
PIN = 'sandbox'
CALLBACK = 'http://127.0.0.1:8000/cart/order/verify-payment/'
BASE_URL = 'https://panel.aqayepardakht.ir/api/v2'


def pg_get_error(error_code):
    match error_code:
        case '0':
            return 'Payment was not made'
        case '1':
            return 'Payment done successfully'
        case '2':
            return 'The transaction has already been verified and paid'
        case '-1':
            return 'amount cannot be empty'
        case '-2':
            return 'pin code cannot be empty'
        case '-3':
            return 'callback cannot be empty'
        case '-4':
            return 'amount should be digit'
        case '-5':
            return 'amount should be between 1000 and 200000000'
        case '-6':
            return 'The pin code  is wrong'
        case '-7':
            return 'trans id cannot be empty'
        case '-8':
            return 'The transaction does not exist'
        case '-9':
            return 'The pin code does not match the transaction pin'
        case '-10':
            return 'The amount does not match the transaction amount'
        case '-11':
            return 'The port is waiting for confirmation or inactive'
        case '-12':
            return 'It is not possible to send a request to this recipient'
        case '-13':
            return 'The card number must be 16 consecutive digits'
        case '-14':
            return 'The port is being used on another site'
        case _:
            return 'Unknown error'


def pg_create(data):
    data = {
        'pin': PIN,
        'amount': data.get('amount'),
        'callback': CALLBACK,
        'invoice_id': data.get('invoice_id'),
    }
    response = requests.post(f'{BASE_URL}/create/',data)
    return response


def pg_verify(data):
    data = {
        'pin': PIN,
        'amount': data.get('amount'),
        'transid': data.get('transid')
    }
    response = requests.post(f'{BASE_URL}/verify/',data)
    return response
