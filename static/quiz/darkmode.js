document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('dark-toggle');
  const html = document.documentElement;
  const thumb = document.getElementById('toggle-thumb');

  // Load theme from localStorage
  if (localStorage.theme === 'dark') {
    html.classList.add('dark');
    thumb.classList.add('translate-x-7');
  }

  toggleBtn.addEventListener('click', () => {
    html.classList.toggle('dark');
    const isDark = html.classList.contains('dark');
    thumb.classList.toggle('translate-x-7');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });
});







// document.addEventListener('DOMContentLoaded', function() {
//     const toggleButton = document.getElementById('toggle-dark-mode');
//     const body = document.getElementById('main-body');

//     const isDarkMode = localStorage.getItem('darkMode') === 'true';  // fixed variable name
//     if (isDarkMode) {
//         body.classList.add('dark');
//     }

//     toggleButton.addEventListener('click', function() {
//         body.classList.toggle('dark');
//         const isDark = body.classList.contains('dark');
//         localStorage.setItem('darkMode', isDark);
//     });
// }); 