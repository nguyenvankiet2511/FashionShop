let products = [];

document.getElementById('addButton').addEventListener('click', function () {
    const selectElement = document.getElementById('productSelect');
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const productName = selectedOption.text; // Lấy nội dung văn bản của tùy chọn đã chọn
    const productValue = document.getElementById('productSelect').value;
    const quantity = document.getElementById('quantity').value;
    const note = document.getElementById('note').value;

    if (!productName || !quantity) {
        alert('Please fill all required fields for the product.');
        return;
    }

    // Thêm sản phẩm vào danh sách
    products.push({productValue, productName, quantity, note });

    // Hiển thị danh sách nếu có sản phẩm
    if (products.length > 0) {
        document.getElementById('productList').style.display = 'block';
    }

    // Cập nhật danh sách sản phẩm trên giao diện
    const productList = products.map(p =>
        `<li class="product-item">
        <input name="product_id" hidden value="${p.productValue}" />
        <input type="text" name="name" value="${p.productName}" readonly />
        <input type="text" name="quantity" value="${p.quantity}" />
        <input type="text" name="note" value="${p.note}" readonly />
        <div class="button-container">
            <input type="button" class="btn btn-danger" onclick="deleteRow(this)" value="Xóa" />
        </div>
        </li>
            `).join('');
    document.getElementById('productList').innerHTML = productList;

    // Reset lại form đơn hàng
    document.getElementById('productSelect').value = '';
    //document.getElementById('quantity').value = '';
    document.getElementById('note').value = '';
});

function deleteRow(button) {
    // Tìm phần tử <li> chứa nút "Xóa"
    const listItem = button.closest('li.product-item');
    const index = Array.from(listItem.parentNode.children).indexOf(listItem);

    // Xóa sản phẩm khỏi danh sách
    products.splice(index, 1);

    // Cập nhật danh sách sản phẩm trên giao diện
    const productList = products.map(p =>
        `<li class="product-item">
        <input name="product_id" hidden value="${p.productValue}" />
        <input type="text" name="name" value="${p.productName}" readonly />
        <input type="text" name="quantity" value="${p.quantity}" />
        <input type="text" name="note" value="${p.note}" readonly />
        <div class="button-container">
            <input type="button" class="btn btn-danger" onclick="deleteRow(this)" value="Xóa" />
        </div>
        </li>
            `).join('');
    document.getElementById('productList').innerHTML = productList;

    // Ẩn danh sách nếu không còn sản phẩm
    if (products.length === 0) {
        document.getElementById('productList').style.display = 'none';
    }
}


document.getElementById('confirmPaymentButton').addEventListener('click', function () {
    const customerId = document.getElementById('customerId').value;
    const customerName = document.getElementById('customerName').value;
    const purchaseDate = document.getElementById('purchaseDate').value;
    const address = document.getElementById('address').value;

    // Kiểm tra nếu chưa điền đủ thông tin khách hàng hoặc chưa có sản phẩm
    if (!customerId || !customerName || !purchaseDate || !address || products.length === 0) {
        alert('Please fill all required fields and add at least one product.');
        return;
    }

    // Thêm dữ liệu khách hàng vào bảng
    const table = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    // Thêm checkbox vào cột đầu tiên
    const checkCell = newRow.insertCell(0);
    const checkBox = document.createElement('input');
    checkBox.type = 'checkbox';
    checkBox.className = 'select-checkbox'; // Thêm lớp để dễ dàng chọn
    checkCell.appendChild(checkBox);

    newRow.insertCell(1).textContent = customerId;
    newRow.insertCell(2).textContent = customerName;
    newRow.insertCell(3).textContent = purchaseDate;
    newRow.insertCell(4).textContent = address;

    // Hiển thị sản phẩm trong cùng một hàng với nhiều dòng
    const productCell = newRow.insertCell(5);
    const quantityCell = newRow.insertCell(6);
    const noteCell = newRow.insertCell(7);

    productCell.innerHTML = products.map(p => `${p.productName}`).join('<br>');
    quantityCell.innerHTML = products.map(p => `${p.quantity}`).join('<br>');
    noteCell.innerHTML = products.map(p => `${p.note}`).join('<br>');

    // Xóa danh sách sản phẩm sau khi submit
    products = [];
    document.getElementById('productList').innerHTML = '';

    // Reset form thông tin khách hàng
    document.getElementById('customerForm').reset();
});

// Xóa các hàng được chọn

document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('productInput');
    var dropdownList = document.getElementById('dropdownList');
    var searchBox = document.getElementById('searchBox');
    var select = document.getElementById('productSelect');

    // Hiển thị danh sách khi người dùng nhấp vào ô nhập
    input.addEventListener('focus', function() {
        dropdownList.style.display = 'block';
    });

    // Ẩn danh sách khi người dùng nhấp ra ngoài
    document.addEventListener('click', function(event) {
        if (!input.contains(event.target) && !dropdownList.contains(event.target)) {
            dropdownList.style.display = 'none';
        }
    });

    // Lọc các tùy chọn dựa trên ô tìm kiếm
    window.filterOptions = function() {
        var filter = searchBox.value.toLowerCase();
        var options = select.options;

        for (var i = 1; i < options.length; i++) { // Bỏ qua mục đầu tiên (Select a product)
            var option = options[i];
            var optionText = option.textContent.toLowerCase();
            option.style.display = optionText.includes(filter) ? '' : 'none';
        }
    };

    // Cập nhật ô nhập với giá trị được chọn và ẩn danh sách
    select.addEventListener('change', function() {
        input.value = select.options[select.selectedIndex].text;
        dropdownList.style.display = 'none';
    });
});