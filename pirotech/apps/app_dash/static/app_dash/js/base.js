document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main_content');

    if (menuToggle && sidebar && mainContent) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            // Opcional: Adicionar uma classe ao main_content para empurrá-lo ou sobrepô-lo
            // mainContent.classList.toggle('shifted');
        });

        // Fechar a sidebar ao clicar fora dela em telas pequenas
        mainContent.addEventListener('click', function() {
            if (sidebar.classList.contains('active') && window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        });
    }
});
