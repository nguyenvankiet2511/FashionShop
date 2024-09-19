// Hàm cập nhật tổng giá sản phẩm dựa trên số lượng và giá
function updateProductTotal(productElement) {
    const priceElement = productElement.querySelector('.product-price');
    const quantityElement = productElement.querySelector('.product-quantity input');
    const linePriceElement = productElement.querySelector('.product-line-price');

    const price = parseFloat(priceElement.textContent) || 0;
    const quantity = parseInt(quantityElement.value, 10) || 0;
    const linePrice = price * quantity;

    linePriceElement.textContent = linePrice.toFixed(2);

    updateCartTotal();
}

// Hàm cập nhật tổng giỏ hàng
function updateCartTotal() {
    let subtotal = 0;
    document.querySelectorAll('.product').forEach(productElement => {
        const linePriceElement = productElement.querySelector('.product-line-price');
        subtotal += parseFloat(linePriceElement.textContent) || 0;
    });

    const tax = subtotal * 0.05; // Thuế 5%
    const shipping = 15.00; // Phí vận chuyển cố định
    const total = subtotal + tax ;

    document.getElementById('cart-subtotal').textContent = subtotal.toFixed(2);
    document.getElementById('cart-tax').textContent = tax.toFixed(2);
    document.getElementById('cart-total').textContent = total.toFixed(2);
}

// Hàm gửi yêu cầu POST để cập nhật số lượng sản phẩm trong giỏ hàng
function updateCartQuantity(inputElement) {
    const cartId = inputElement.getAttribute('data-cart-id');
    const newQuantity = inputElement.value;

    // Kiểm tra giá trị của cartId và newQuantity
    console.log('Updating cart quantity for cartId:', cartId, 'to quantity:', newQuantity);

    fetch('http://localhost:5001/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            cart_id: cartId,
            quantity: newQuantity
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            console.log('Success:', data.message);
            updateProductTotal(inputElement.closest('.product'));
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function checkOutError(userId) {

            alert("Bạn chưa có sản phẩm để thanh toán! Vui lòng chọn sản phẩm.");
            }


// Hàm xóa sản phẩm khỏi giỏ hàng và cập nhật tổng giỏ hàng
function removeProduct(productElement) {
    productElement.remove();
    updateCartTotal();
}

// Hàm gửi yêu cầu DELETE để xóa sản phẩm khỏi giỏ hàng
function removeToCart(cartId) {
    fetch(`http://localhost:5001/cart/remove?cart_id=${cartId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to remove from cart');
        }
    })
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorDialog('Bạn chưa đăng nhập! Đăng nhập ngay?');
    });
}

// Gán sự kiện cho các ô nhập số lượng và nút xóa sản phẩm
document.querySelectorAll('.product').forEach(productElement => {
    const quantityInput = productElement.querySelector('.product-quantity input');
    const removeButton = productElement.querySelector('.remove-product');

    quantityInput.addEventListener('change', function() {
        updateProductTotal(productElement);
        updateCartQuantity(productElement.dataset.cartId, this.value);
    });

    removeButton.addEventListener('click', function() {
        removeProduct(productElement);
    });
});

// Tính toán tổng giỏ hàng khi tải trang
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.product').forEach(productElement => {
        updateProductTotal(productElement);
    });
});

// jQuery để xử lý các tính năng giao diện
jQuery(document).ready(function($) {
    "use strict";

    var header = $('.header');
    var topNav = $('.top_nav');
    var hamburger = $('.hamburger_container');
    var menu = $('.hamburger_menu');
    var menuActive = false;
    var hamburgerClose = $('.hamburger_close');
    var fsOverlay = $('.fs_menu_overlay');

    function setHeader() {
        if (window.innerWidth < 992) {
            if ($(window).scrollTop() > 100) {
                header.css({ 'top': "0" });
            } else {
                header.css({ 'top': "0" });
            }
        } else {
            if ($(window).scrollTop() > 100) {
                header.css({ 'top': "-50px" });
            } else {
                header.css({ 'top': "0" });
            }
        }
        if (window.innerWidth > 991 && menuActive) {
            closeMenu();
        }
    }

    function initMenu() {
        if (hamburger.length) {
            hamburger.on('click', function() {
                if (!menuActive) {
                    openMenu();
                }
            });
        }
        if (fsOverlay.length) {
            fsOverlay.on('click', function() {
                if (menuActive) {
                    closeMenu();
                }
            });
        }
        if (hamburgerClose.length) {
            hamburgerClose.on('click', function() {
                if (menuActive) {
                    closeMenu();
                }
            });
        }
        if ($('.menu_item').length) {
            var items = document.getElementsByClassName('menu_item');
            var i;
            for (i = 0; i < items.length; i++) {
                if (items[i].classList.contains("has-children")) {
                    items[i].onclick = function() {
                        this.classList.toggle("active");
                        var panel = this.children[1];
                        if (panel.style.maxHeight) {
                            panel.style.maxHeight = null;
                        } else {
                            panel.style.maxHeight = panel.scrollHeight + "px";
                        }
                    }
                }
            }
        }
    }

    function openMenu() {
        menu.addClass('active');
        fsOverlay.css('pointer-events', "auto");
        menuActive = true;
    }

    function closeMenu() {
        menu.removeClass('active');
        fsOverlay.css('pointer-events', "none");
        menuActive = false;
    }

    function initThumbnail() {
        if ($('.single_product_thumbnails ul li').length) {
            var thumbs = $('.single_product_thumbnails ul li');
            var singleImage = $('.single_product_image_background');

            thumbs.each(function() {
                var item = $(this);
                item.on('click', function() {
                    thumbs.removeClass('active');
                    item.addClass('active');
                    var img = item.find('img').data('image');
                    singleImage.css('background-image', 'url(' + img + ')');
                });
            });
        }
    }

    function initQuantity() {
        if ($('.plus').length && $('.minus').length) {
            var plus = $('.plus');
            var minus = $('.minus');
            var value = $('#quantity_value');

            plus.on('click', function() {
                var x = parseInt(value.text(), 10);
                value.text(x + 1);
            });

            minus.on('click', function() {
                var x = parseInt(value.text(), 10);
                if (x > 1) {
                    value.text(x - 1);
                }
            });
        }
    }

    function initStarRating() {
        if ($('.user_star_rating li').length) {
            var stars = $('.user_star_rating li');

            stars.each(function() {
                var star = $(this);

                star.on('click', function() {
                    var i = star.index();

                    stars.find('i').each(function() {
                        $(this).removeClass('fa-star');
                        $(this).addClass('fa-star-o');
                    });
                    for (var x = 0; x <= i; x++) {
                        $(stars[x]).find('i').removeClass('fa-star-o');
                        $(stars[x]).find('i').addClass('fa-star');
                    }
                });
            });
        }
    }

    function initFavorite() {
        if ($('.user_favorite').length) {
            $('.user_favorite').on('click', function() {
                $(this).toggleClass('active');
            });
        }
    }

    function initTabs() {
        if ($('.tabs').length) {
            var tabs = $('.tabs');

            tabs.each(function() {
                var tab = $(this);
                var tabLinks = tab.find('.tab_link');
                var tabContents = tab.find('.tab_content');

                tabLinks.on('click', function(e) {
                    e.preventDefault();
                    var target = $(this).attr('href');

                    tabLinks.removeClass('active');
                    $(this).addClass('active');
                    tabContents.removeClass('active');
                    $(target).addClass('active');
                });
            });
        }
    }

    // Khởi tạo các tính năng khi tải trang
    $(document).ready(function() {
        setHeader();
        $(window).on('resize', setHeader);
        $(document).on('scroll', setHeader);
        initMenu();
        initThumbnail();
        initQuantity();
        initStarRating();
        initFavorite();
        initTabs();
    });
});
