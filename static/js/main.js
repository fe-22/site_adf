// Menu mobile
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('aberto');
    });

    // Fecha menu ao clicar em um link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => navLinks.classList.remove('aberto'));
    });
}

// Lightbox da galeria
function abrirLightbox(src, titulo) {
    const lb = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    const tit = document.getElementById('lightbox-titulo');
    if (!lb) return;
    img.src = src;
    img.alt = titulo;
    if (tit) tit.textContent = titulo;
    lb.classList.add('aberto');
    document.body.style.overflow = 'hidden';
}

function fecharLightbox() {
    const lb = document.getElementById('lightbox');
    if (!lb) return;
    lb.classList.remove('aberto');
    document.body.style.overflow = '';
}

// Fechar lightbox com tecla ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') fecharLightbox();
});
