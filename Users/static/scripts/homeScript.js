const checkbox = document.getElementById('open-menu');
const navLinks = document.querySelectorAll('.header__nav-item a');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        checkbox.checked = false;
    });
});
