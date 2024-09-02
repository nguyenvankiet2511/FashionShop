/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits



******************************/
/*

	search sự kiện

	*/
document.getElementById('search-icon').addEventListener('click', function() {
    var searchBox = document.getElementById('search-box');
    searchBox.classList.toggle('show');
});

/*

	đánh giá sự kiện

	*/
	document.addEventListener('DOMContentLoaded', function() {
		var starElements = document.querySelectorAll('.star_rating span');
		var selectedRating = 0;

		// Thêm sự kiện hover cho các sao
		starElements.forEach(function(star) {
			star.addEventListener('mouseover', function() {
				var rating = this.getAttribute('data-rating');
				highlightStars(rating);
			});

			star.addEventListener('mouseout', function() {
				highlightStars(selectedRating);
			});

			star.addEventListener('click', function() {
				selectedRating = this.getAttribute('data-rating');
				highlightStars(selectedRating);
			});
		});

		function highlightStars(rating) {
			starElements.forEach(function(star) {
				var starRating = star.getAttribute('data-rating');
				if (starRating <= rating) {
					star.classList.add('hover');
				} else {
					star.classList.remove('hover');
				}
			});
		}

		// Xử lý sự kiện gửi mẫu
		document.getElementById('feedback_form').addEventListener('submit', function(event) {
			event.preventDefault(); // Ngăn gửi mẫu mặc định

			// Lấy thông tin từ các trường nhập
			var name = document.getElementById('input_name').value;
			var email = document.getElementById('input_email').value;
			var message = document.getElementById('input_message').value;
			var rating = selectedRating;

			// Xử lý gửi dữ liệu đến server
			fetch('your-server-endpoint', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					name: name,
					email: email,
					message: message,
					rating: rating
				})
			})
			.then(response => response.json())
			.then(data => {
				alert('Feedback sent successfully!');
				// Xóa hoặc reset các trường nhập và đánh giá nếu cần
				document.getElementById('input_name').value = '';
				document.getElementById('input_email').value = '';
				document.getElementById('input_message').value = '';
				selectedRating = 0;
				highlightStars(selectedRating);

				// Cập nhật danh sách đánh giá (có thể tải lại dữ liệu từ server)
				updateReviews();
			})
			.catch(error => {
				alert('There was an error sending your feedback.');
				console.error('Error:', error);
			});
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
	var map;

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
	initGoogleMap();

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


});