import os
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env
load_dotenv()

class Config:
    # Cấu hình VNPay
    VNPAY_TMN_CODE = os.getenv('VNPAY_TMN_CODE')
    VNPAY_HASH_SECRET = os.getenv('VNPAY_HASH_SECRET')
    VNPAY_URL = os.getenv('VNPAY_URL', 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html')
    VNPAY_RETURN_URL = os.getenv('VNPAY_RETURN_URL', 'http://localhost:8000/payment_return')  # Đã chỉnh sửa cổng từ 5000 thành 8000 để khớp với mặc định của Django
    VNPAY_VERSION = '2.1.0'
    VNPAY_COMMAND = 'pay'
    VNPAY_CURRENCY_CODE = 'VND'
    VNPAY_LOCALE = 'vn'

# Hàm để sử dụng các cấu hình khi cần
def get_vnpay_config():
    return {
        'vnp_TmnCode': Config.VNPAY_TMN_CODE,
        'vnp_HashSecret': Config.VNPAY_HASH_SECRET,
        'vnp_Url': Config.VNPAY_URL,
        'vnp_ReturnUrl': Config.VNPAY_RETURN_URL,
        'vnp_Version': Config.VNPAY_VERSION,
        'vnp_Command': Config.VNPAY_COMMAND,
        'vnp_CurrCode': Config.VNPAY_CURRENCY_CODE,
        'vnp_Locale': Config.VNPAY_LOCALE
    }
