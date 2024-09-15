document.addEventListener('DOMContentLoaded', function() {
    const payButton = document.getElementById('payButton');
    const generateQRButton = document.getElementById('generateQR');
    const qrCodeContainer = document.getElementById('qrCodeContainer');

    // Số tiền cố định, thay đổi nếu cần
    const amount = 100000; // Ví dụ: 100,000 VND

    if (payButton) {
        payButton.addEventListener('click', function() {
            // Tạo URL thanh toán với số tiền đã định
            const paymentUrl = `/payment?amount=${amount}`;
            window.location.href = paymentUrl;
        });
    }

    if (generateQRButton) {
        generateQRButton.addEventListener('click', function() {
            const qrCodeUrl = generateQRCodeUrl(amount);
            qrCodeContainer.innerHTML = `<img src="${qrCodeUrl}" alt="QR Code">`;
        });
    }
});

function generateQRCodeUrl(amount) {
    // Thay đổi URL và tham số theo cách mà mã QR được tạo ra trong thực tế
    return `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=ThanhToan%20${encodeURIComponent(amount)}`;
}
