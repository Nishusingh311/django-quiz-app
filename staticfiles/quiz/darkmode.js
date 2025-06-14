
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-dark-mode');
    const body = document.getElementById('main-body');

    const isDarkMode = localStorage.getItem('darkMode') === 'true';  // fixed variable name
    if (isDarkMode) {
        body.classList.add('dark');
    }

    toggleButton.addEventListener('click', function() {
        body.classList.toggle('dark');
        const isDark = body.classList.contains('dark');
        localStorage.setItem('darkMode', isDark);
    });
}); 