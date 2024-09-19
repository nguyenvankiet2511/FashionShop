/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Menu
4. Init Thumbnail
5. Init Quantity
6. Init Star Rating
7. Init Favorite
8. Init Tabs



******************************/
/*Lấy giá trị quanlity*/
  function getQuantity() {
        return document.getElementById('quantity_value').innerText;
    }

    function addToCartSingle(productId, quantity) {
        fetch(`http://localhost:5001/cart/add?product_id=${productId}&quantity=${quantity}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to add to cart');
            }
        })
        .then(data => {
            // Thông báo khi thêm vào giỏ hàng thành công
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            // Hiển thị hộp thoại lỗi với tùy chọn đăng nhập
            showErrorDialog('Bạn chưa đăng nhập! Đăng nhập ngay?');
        });
    }

    function showErrorDialog(message) {
        // Tạo phần tử div cho hộp thoại nếu chưa tồn tại
        let dialog = document.getElementById('errorDialog');
        if (!dialog) {
            dialog = document.createElement('div');
            dialog.id = 'errorDialog';
            dialog.style.position = 'fixed';
            dialog.style.top = '80px'; // Đặt vị trí trung tâm theo chiều dọc
            dialog.style.left = '50%'; // Đặt vị trí trung tâm theo chiều ngang
            dialog.style.transform = 'translate(-50%, -50%)'; // Điều chỉnh để trung tâm chính xác
            dialog.style.width = '400px'; // Đặt chiều rộng của hộp thoại
            dialog.style.padding = '20px';
            dialog.style.borderRadius = '8px'; // Bo tròn các góc
            dialog.style.border = '1px solid #ccc';
            dialog.style.background = '#fff';
            dialog.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
            dialog.style.zIndex = '1000';
            dialog.style.display = 'none';
            dialog.style.textAlign = 'center'; // Căn giữa văn bản
            document.body.appendChild(dialog);
        }

        // Cập nhật nội dung hộp thoại
        dialog.innerHTML = `
            <p id="errorMessage" style="margin-bottom: 20px;">${message}</p>
            <button onclick="redirectToLogin()" style="margin-right: 10px; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Đăng nhập ngay</button>
            <button onclick="closeDialog()" style="padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Hủy</button>
        `;

        // Hiển thị hộp thoại
        dialog.style.display = 'block';
    }

    function redirectToLogin() {
        // Thay đổi URL đến trang đăng nhập
        window.location.href = 'http://localhost:5001/login';
    }

    function closeDialog() {
        const dialog = document.getElementById('errorDialog');
        if (dialog) {
            dialog.style.display = 'none';
        }
    }
document.getElementById('search-icon').addEventListener('click', function() {
    var searchBox = document.getElementById('search-box');
    searchBox.classList.toggle('show');
});
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('review_form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn gửi form theo cách mặc định

        // Lấy dữ liệu từ các trường trong form
        var name = document.getElementById('review_name').value;
        var email = document.getElementById('review_email').value;
        var message = document.getElementById('review_message').value;

        // Đếm số sao được chọn
        var rating = document.querySelectorAll('.user_star_rating li.fa-star').length;

        // Kiểm tra nếu các trường không rỗng
        if(name && email && message) {
            // Gửi dữ liệu thông qua fetch API
            fetch('submit_review.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'name': name,
                    'email': email,
                    'message': message,
                    'rating': rating
                })
            })
            .then(response => response.text())
            .then(data => {
                alert('Cảm ơn bạn đã gửi đánh giá!');
                document.getElementById('review_form').reset(); // Reset form
            })
            .catch(error => {
                alert('Có lỗi xảy ra, vui lòng thử lại sau.');
                console.error('Error:', error);
            });
        } else {
            alert('Vui lòng điền đầy đủ thông tin.');
        }
    });
});

// sự kiện tăng tiền theo só lượng sản phẩm chọn
document.addEventListener('DOMContentLoaded', function() {
    const quantityValue = document.getElementById('quantity_value');
    const totalPriceElement = document.getElementById('total_price');
    const originalPriceElement = document.getElementById('original_price');

    let quantity = parseInt(quantityValue.textContent);
    const originalPrice = parseFloat(originalPriceElement.getAttribute('data-price'));

    document.querySelector('.plus').addEventListener('click', function() {
        quantity++;
        quantityValue.textContent = quantity;
        updateTotalPrice();
    });

    document.querySelector('.minus').addEventListener('click', function() {
        if (quantity > 1) {
            quantity--;
            quantityValue.textContent = quantity;
            updateTotalPrice();
        }
    });

    function updateTotalPrice() {
        const totalPrice = originalPrice * quantity;
        totalPriceElement.textContent = `${totalPrice.toFixed(2)} VND`;
    }
});


// sự kiện thêm vào giỏ hàng











// sự kiện thanh toán chuyển sang trang pay ment

document.addEventListener('DOMContentLoaded', function() {
    // Chọn nút bằng ID
    const paymentButton = document.getElementById('payment_button');

    // Thêm sự kiện click cho nút
    paymentButton.addEventListener('click', function() {
        // Chuyển hướng đến trang thanh toán
        window.location.href = 'contact.html'; // Thay 'payment_page.html' bằng đường dẫn đến trang thanh toán của bạn
    });
});









jQuery(document).ready(function($)
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var topNav = $('.top_nav')
	var hamburger = $('.hamburger_container');
	var menu = $('.hamburger_menu');
	var menuActive = false;
	var hamburgerClose = $('.hamburger_close');
	var fsOverlay = $('.fs_menu_overlay');

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initMenu();
	initThumbnail();
	initQuantity();
	initStarRating();
	initFavorite();
	initTabs();

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if(window.innerWidth < 992)
		{
			if($(window).scrollTop() > 100)
			{
				header.css({'top':"0"});
			}
			else
			{
				header.css({'top':"0"});
			}
		}
		else
		{
			if($(window).scrollTop() > 100)
			{
				header.css({'top':"-50px"});
			}
			else
			{
				header.css({'top':"0"});
			}
		}
		if(window.innerWidth > 991 && menuActive)
		{
			closeMenu();
		}
	}

	/* 

	3. Init Menu

	*/

	function initMenu()
	{
		if(hamburger.length)
		{
			hamburger.on('click', function()
			{
				if(!menuActive)
				{
					openMenu();
				}
			});
		}

		if(fsOverlay.length)
		{
			fsOverlay.on('click', function()
			{
				if(menuActive)
				{
					closeMenu();
				}
			});
		}

		if(hamburgerClose.length)
		{
			hamburgerClose.on('click', function()
			{
				if(menuActive)
				{
					closeMenu();
				}
			});
		}

		if($('.menu_item').length)
		{
			var items = document.getElementsByClassName('menu_item');
			var i;

			for(i = 0; i < items.length; i++)
			{
				if(items[i].classList.contains("has-children"))
				{
					items[i].onclick = function()
					{
						this.classList.toggle("active");
						var panel = this.children[1];
					    if(panel.style.maxHeight)
					    {
					    	panel.style.maxHeight = null;
					    }
					    else
					    {
					    	panel.style.maxHeight = panel.scrollHeight + "px";
					    }
					}
				}	
			}
		}
	}

	function openMenu()
	{
		menu.addClass('active');
		// menu.css('right', "0");
		fsOverlay.css('pointer-events', "auto");
		menuActive = true;
	}

	function closeMenu()
	{
		menu.removeClass('active');
		fsOverlay.css('pointer-events', "none");
		menuActive = false;
	}

	/* 

	4. Init Thumbnail

	*/

	function initThumbnail()
	{
		if($('.single_product_thumbnails ul li').length)
		{
			var thumbs = $('.single_product_thumbnails ul li');
			var singleImage = $('.single_product_image_background');

			thumbs.each(function()
			{
				var item = $(this);
				item.on('click', function()
				{
					thumbs.removeClass('active');
					item.addClass('active');
					var img = item.find('img').data('image');
					singleImage.css('background-image', 'url(' + img + ')');
				});
			});
		}	
	}

	/* 

	5. Init Quantity

	*/

	function initQuantity()
	{
		if($('.plus').length && $('.minus').length)
		{
			var plus = $('.plus');
			var minus = $('.minus');
			var value = $('#quantity_value');

			plus.on('click', function()
			{
				var x = parseInt(value.text());
				value.text(x + 1);
			});

			minus.on('click', function()
			{
				var x = parseInt(value.text());
				if(x > 1)
				{
					value.text(x - 1);
				}
			});
		}
	}

	/* 

	6. Init Star Rating

	*/

	function initStarRating()
	{
		if($('.user_star_rating li').length)
		{
			var stars = $('.user_star_rating li');

			stars.each(function()
			{
				var star = $(this);

				star.on('click', function()
				{
					var i = star.index();

					stars.find('i').each(function()
					{
						$(this).removeClass('fa-star');
						$(this).addClass('fa-star-o');
					});
					for(var x = 0; x <= i; x++)
					{
						$(stars[x]).find('i').removeClass('fa-star-o');
						$(stars[x]).find('i').addClass('fa-star');
					};
				});
			});
		}
	}

	/* 

	7. Init Favorite

	*/

	function initFavorite()
	{
		if($('.product_favorite').length)
		{
			var fav = $('.product_favorite');

			fav.on('click', function()
			{
				fav.toggleClass('active');
			});
		}
	}

	/* 

	8. Init Tabs

	*/

	function initTabs()
	{
		if($('.tabs').length)
		{
			var tabs = $('.tabs li');
			var tabContainers = $('.tab_container');

			tabs.each(function()
			{
				var tab = $(this);
				var tab_id = tab.data('active-tab');

				tab.on('click', function()
				{
					if(!tab.hasClass('active'))
					{
						tabs.removeClass('active');
						tabContainers.removeClass('active');
						tab.addClass('active');
						$('#' + tab_id).addClass('active');
					}
				});
			});
		}
	}
});