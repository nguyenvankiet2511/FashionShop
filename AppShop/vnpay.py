import hashlib
import hmac
import urllib.parse
from datetime import datetime, timedelta

class vnpay:
    def __init__(self):
        self.requestData = {}
        self.responseData = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        # Sắp xếp các tham số theo thứ tự
        inputData = sorted(self.requestData.items())
        queryString = ''
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString += "&" + key + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                queryString = key + '=' + urllib.parse.quote_plus(str(val))

        # Tạo mã bảo mật HMAC-SHA512
        hashValue = self.__hmacsha512(secret_key, queryString)
        return vnpay_payment_url + "?" + queryString + '&vnp_SecureHash=' + hashValue

    def validate_response(self, secret_key):
        vnp_SecureHash = self.responseData.get('vnp_SecureHash', '')
        # Xóa các tham số mã bảo mật
        self.responseData.pop('vnp_SecureHash', None)
        self.responseData.pop('vnp_SecureHashType', None)

        # Sắp xếp các tham số theo thứ tự
        inputData = sorted(self.responseData.items())
        hasData = ''
        seq = 0
        for key, val in inputData:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData += "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                else:
                    seq = 1
                    hasData = str(key) + '=' + urllib.parse.quote_plus(str(val))

        # Tạo mã bảo mật HMAC-SHA512
        hashValue = self.__hmacsha512(secret_key, hasData)
        print(
            'Validate debug, HashData:' + hasData + "\n HashValue:" + hashValue + "\nInputHash:" + vnp_SecureHash
        )

        return vnp_SecureHash == hashValue

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode('utf-8')
        byteData = data.encode('utf-8')
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

def generate_vnpay_url(amount, transaction_ref):
    vnp = vnpay()
    vnp.requestData = {
        'vnp_Version': '2.1.0',
        'vnp_TmnCode': 'your_merchant_id',
        'vnp_Amount': amount * 100,  # VNPay yêu cầu số tiền tính bằng đồng (VND)
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': transaction_ref,
        'vnp_OrderInfo': 'Thanh toán đơn hàng',
        'vnp_OrderType': 'other',
        'vnp_ReturnUrl': 'http://your-domain.com/payment_return',
        'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
        'vnp_ExpireDate': (datetime.now() + timedelta(minutes=15)).strftime('%Y%m%d%H%M%S'),
    }

    # Thay đổi URL thanh toán và key bí mật
    vnpay_payment_url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    secret_key = 'your_secret_key'
    vnp_url = vnp.get_payment_url(vnpay_payment_url, secret_key)
    return vnp_url
