$(document).ready(function () {
    // Xử lý sự kiện chuyển đổi tab
    $('#register-link').click(function (e) {
        e.preventDefault();
        $('.tab-content .tab-pane').removeClass('show active');
        $('#pills-register').addClass('show active');
    });
    $('#login-link').click(function (e) {
        e.preventDefault();
        $('.tab-content .tab-pane').removeClass('show active');
        $('#pills-login').addClass('show active');
    });
    $('#forgot-link').click(function (e) {
        e.preventDefault();
        $('.tab-content .tab-pane').removeClass('show active');
        $('#pills-forgot').addClass('show active');
    });
    $('#back-to-login').click(function (e) {
        e.preventDefault();
        $('.tab-content .tab-pane').removeClass('show active');
        $('#pills-login').addClass('show active');
    });

    // Hiệu ứng gõ chữ cho tất cả các placeholder
    const inputs = document.querySelectorAll('input[placeholder]');
    inputs.forEach(input => {
        const placeholderText = input.placeholder;
        let charIndex = 0;
        function typePlaceholder() {
            input.placeholder = placeholderText.substring(0, charIndex);
            charIndex++;
            if (charIndex > placeholderText.length) {
                // Reset và bắt đầu lại
                charIndex = 0;
                setTimeout(() => {
                    typePlaceholder();
                }, 1000); // Độ trễ trước khi bắt đầu lại
            } else {
                setTimeout(typePlaceholder, 100); // Độ trễ giữa các ký tự
            }
        }
        typePlaceholder(); // Bắt đầu hiệu ứng gõ chữ
    });

    // Xử lý sự kiện gửi form đăng ký
    document.getElementById('registerForm').addEventListener('submit', function (event) {
       // Ngăn chặn hành động gửi form mặc định
        // Lấy dữ liệu từ form
        const email = document.getElementById('registerEmail').value;
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('registerConfirmPassword').value;
        const registrationMessage = document.getElementById('registration-message');
        // Biểu thức chính quy kiểm tra email
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        // Kiểm tra cú pháp email
        if (!emailPattern.test(email)) {
            registrationMessage.textContent = 'Please enter a valid email address.';
            registrationMessage.style.color = 'red';
            return;
        }
        // Kiểm tra mật khẩu và xác nhận mật khẩu
        if (password !== confirmPassword) {
            registrationMessage.textContent = 'Passwords do not match.';
            registrationMessage.style.color = 'red';
            return;
        }
        // Nếu tất cả đều hợp lệ, hiển thị thông báo thành công
        registrationMessage.textContent = 'Registration successful!';
        registrationMessage.style.color = 'green';
        // Đặt lại form

    });

    // Xử lý sự kiện gửi form quên mật khẩu
    document.getElementById('forgotForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Ngăn chặn hành động gửi form mặc định
        const forgotMessage = document.getElementById('forgot-message');
        forgotMessage.textContent = 'Password reset link has been sent!';
        forgotMessage.style.color = 'green';
        // Đặt lại form
        document.getElementById('forgotForm').reset();
    });
});
