document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main');
    const dropdownToggles = document.querySelectorAll('.nav-item.dropdown');
    
    // Toggle sidebar visibility and adjust main content
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed'); // Toggle collapsed state

        if (sidebar.classList.contains('collapsed')) {
            sidebar.style.transform = 'translateX(-250px)'; // Hide sidebar
            mainContent.style.marginLeft = '0'; // Expand main content
        } else {
            sidebar.style.transform = 'translateX(0)'; // Show sidebar
            mainContent.style.marginLeft = '250px'; // Adjust main content margin
        }
    });

    // Toggle dropdown menus
    dropdownToggles.forEach(item => {
        const dropdownMenu = item.querySelector('.dropdown-menu');
        if (dropdownMenu) {
            item.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent event from bubbling up
                dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
            });
        }
    });

    // Hide dropdown menu when clicking outside
    document.addEventListener('click', (e) => {
        dropdownToggles.forEach(item => {
            const dropdownMenu = item.querySelector('.dropdown-menu');
            if (dropdownMenu && dropdownMenu.style.display === 'block' && !item.contains(e.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
    });
});

document.querySelector('.search-btn').addEventListener('click', function() {
    const container = document.querySelector('.search-container');
    const input = container.querySelector('.search-input');
    container.classList.toggle('active');
    input.focus(); // Optional: Focus on the input when it expands
});

