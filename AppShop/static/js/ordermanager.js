
 function getCheckedOrderIds() {
        let selectedOrderIds = [];
        // Lấy tất cả các checkbox đã được chọn
        const checkboxes = document.querySelectorAll('.checkthis:checked');
        checkboxes.forEach(function(checkbox) {
            const orderId = checkbox.closest('tr').getAttribute('data-id');
            selectedOrderIds.push(orderId);
        });
        return selectedOrderIds;
    }
document.getElementById('confirmSelected1').addEventListener('click', function (event) {
        event.preventDefault();  // Ngăn chặn hành động mặc định của nút

        let checkedOrderIds = getCheckedOrderIds();
        if (checkedOrderIds.length > 0) {
            let orderIdsStr = checkedOrderIds.join(',');  // Chuyển danh sách thành chuỗi ngăn cách bởi dấu phẩy

            // Tạo URL động với danh sách ID và cập nhật thẻ <a>
            const confirmUrl = `/employee/confirm-order-list?list_id=${orderIdsStr}`;
            document.getElementById('confirmSelectedLink').setAttribute('href', confirmUrl);

            // Chuyển hướng đến URL mới
            window.location.href = confirmUrl;
        } else {
            alert('Please select at least one order to proceed.');
        }
    });
// Function to search in the table
function searchTable(tableId) {
    const input = document.getElementById(`searchInput${tableId.replace('mytable', '')}`);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const trs = table.querySelectorAll('tbody tr');

    trs.forEach(tr => {
        const td = tr.getElementsByTagName('td');
        let match = false;
        for (let i = 1; i < td.length; i++) { // Skip the first column (checkbox column)
            if (td[i].textContent.toUpperCase().indexOf(filter) > -1) {
                match = true;
                break;
            }
        }
        tr.style.display = match ? '' : 'none';
    });
}



document.addEventListener('DOMContentLoaded', () => {
    const showModal = (modalId) => {
        // Ẩn tất cả các modal
        document.querySelectorAll('.modal').forEach(modal => {
            $(modal).modal('hide');
        });
        // Hiển thị modal mới
        $(`#${modalId}`).modal('show');
    };

    const searchTable = (tableId) => {
        const input = document.getElementById(`searchInput${tableId}`);
        const filter = input.value.toLowerCase();
        const table = document.getElementById(tableId);
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        Array.from(rows).forEach(row => {
            const cells = row.getElementsByTagName('td');
            let match = false;
            Array.from(cells).forEach(cell => {
                if (cell.textContent.toLowerCase().includes(filter)) {
                    match = true;
                }
            });
            row.style.display = match ? '' : 'none';
        });
    };

    const handleDeleteSelected = () => {
        const checkboxes = document.querySelectorAll('#mytable1 .checkthis:checked');
        if (checkboxes.length > 0) {
            showModal('deleteModal');
        }
    };

    const handleConfirmSelected = () => {
        const checkboxes = document.querySelectorAll('#mytable1 .checkthis:checked');
        if (checkboxes.length > 0) {
            showModal('confirmApproveModal');
        }
    };

    const handleEdit = (id) => {
        showModal('editModal');
        // Populate edit form based on the id
    };

    const handleDelete = (id) => {
        showModal('deleteModal');
        // Handle single delete logic
    };

    const handleConfirm = (id) => {
        showModal('confirmApproveModal');
        // Handle single confirm logic
    };

    document.getElementById('checkall1').addEventListener('change', (event) => {
        const checked = event.target.checked;
        document.querySelectorAll('#mytable1 .checkthis').forEach(checkbox => checkbox.checked = checked);
    });

    document.getElementById('deleteSelected1').addEventListener('click', handleDeleteSelected);
    document.getElementById('confirmSelected1').addEventListener('click', handleConfirmSelected);

    document.querySelectorAll('#mytable1 .edit-btn').forEach(button => {
        button.addEventListener('click', (event) => handleEdit(event.target.dataset.id));
    });

    document.querySelectorAll('#mytable1 .delete-btn').forEach(button => {
        button.addEventListener('click', (event) => handleDelete(event.target.dataset.id));
    });

    document.querySelectorAll('#mytable1 .confirm-btn').forEach(button => {
        button.addEventListener('click', (event) => handleConfirm(event.target.dataset.id));
    });

    document.getElementById('confirmDelete').addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('#mytable1 .checkthis:checked');
        checkboxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            row.remove(); // Remove row from the DOM
        });
        $('#deleteModal').modal('hide');
    });

    document.getElementById('confirmApproveButton').addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('#mytable1 .checkthis:checked');
        checkboxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            const clone = row.cloneNode(true); // Clone the row

            // Hide specific columns in the cloned row
            clone.querySelectorAll('td:nth-child(1), td:nth-child(10), td:nth-child(11), td:nth-child(12)').forEach(cell => cell.style.display = 'none');

            // Add the row to the "Confirmed Orders" table
            document.querySelector('#mytable2 tbody').appendChild(clone);
            
            // Remove the row from the original table
            row.remove(); 
        });
        $('#confirmApproveModal').modal('hide');
    });
});


function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function closeModalOnClickOutside(event, modalId) {
    if (event.target === document.getElementById(modalId)) {
        closeModal(modalId);
    }
}

function showModal(modalId) {
    // Ẩn tất cả các modal
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
    // Hiển thị modal mới
    document.getElementById(modalId).style.display = 'block';
}



