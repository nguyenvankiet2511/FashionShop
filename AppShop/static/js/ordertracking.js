document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([10.762622, 106.660172], 13); // Trung tâm bản đồ
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var marker;

    function updateMap() {
        var address = document.getElementById('shipping-address').textContent; // Lấy giá trị từ thẻ <span>
        var geocodeUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`;
        fetch(geocodeUrl)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    var lat = data[0].lat;
                    var lon = data[0].lon;
                    var location = [lat, lon];
                    map.setView(location, 13);
                    if (marker) {
                        marker.setLatLng(location);
                    } else {
                        marker = L.marker(location).addTo(map);
                    }
                    marker.bindPopup(address).openPopup();
                } else {
                    alert('Không tìm thấy địa chỉ.');
                }
            })
            .catch(error => {
                console.error('Lỗi:', error);
                alert('Lỗi khi tìm kiếm địa chỉ.');
            });
    }

    document.getElementById('update-map').addEventListener('click', updateMap);
    updateMap(); // Cập nhật bản đồ khi tải xong
});

document.addEventListener('DOMContentLoaded', function() {
    var timelineItems = document.querySelectorAll('.timeline-item');
    var orderDateInput = document.getElementById('order-date');
    var updateButton = document.getElementById('update-progress');

    function updateTimeline() {
        var orderDate = new Date(orderDateInput.value);
        
        timelineItems.forEach(function(item) {
            var daysOffset = parseInt(item.getAttribute('data-days'));
            var time = item.getAttribute('data-time');

            // Tính ngày và thời gian cụ thể
            var eventDate = new Date(orderDate);
            eventDate.setDate(orderDate.getDate() + daysOffset);

            var options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
            var formattedDate = eventDate.toLocaleDateString('vi-VN', options);

            item.querySelector('.timeline-content p').textContent = formattedDate + ', ' + time;
        });
    }

    // Cập nhật tiến trình khi nhấp vào nút "Cập nhật tiến trình"
    updateButton.addEventListener('click', function() {
        updateTimeline();
    });

    // Cập nhật tiến trình khi ngày đặt hàng thay đổi
    orderDateInput.addEventListener('change', function() {
        updateTimeline();
    });

    // Cập nhật tiến trình ban đầu
    updateTimeline();

    // Thêm sự kiện click cho các mục timeline để hiển thị thông tin chi tiết
    timelineItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Đóng tất cả các mục hiện tại
            timelineItems.forEach(function(otherItem) {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });

            // Chuyển đổi trạng thái của mục hiện tại
            this.classList.toggle('active');
            
            // Hiển thị thông tin thời gian
            var daysOffset = parseInt(this.getAttribute('data-days'));
            var time = this.getAttribute('data-time');
            var eventDate = new Date(orderDateInput.value);
            eventDate.setDate(eventDate.getDate() + daysOffset);
            var formattedDate = eventDate.toLocaleDateString('vi-VN', { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });

            this.querySelector('.timeline-content p').textContent = formattedDate + ', ' + time;
        });
    });
});










u