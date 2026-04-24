const gallery = document.querySelector('.gallery');
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const closeBtn = document.getElementById('modal-close');
const prevBtn = document.getElementById('modal-prev');
const nextBtn = document.getElementById('modal-next');

const images = Array.from(document.querySelectorAll('.gallery img'));
let currentIndex = 0;

function openModal(index) {
    currentIndex = index;
    const fullUrl = images[index].dataset.full;
    modalImg.src = fullUrl;
    modal.classList.remove('hidden');
}

function closeModal() { modal.classList.add('hidden'); }

function showPrev() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    modalImg.src = images[currentIndex].dataset.full;
}

function showNext() {
    currentIndex = (currentIndex + 1) % images.length;
    modalImg.src = images[currentIndex].dataset.full;
}

// Event delegation — клик на галерею
gallery.addEventListener('click', (e) => {
    const img = e.target.closest('img');
    if (!img) return;
    const index = images.indexOf(img);
    openModal(index);
});

closeBtn.addEventListener('click', closeModal);
prevBtn.addEventListener('click', showPrev);
nextBtn.addEventListener('click', showNext);

// Закрытие по клику на overlay
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

// Клавиатура
document.addEventListener('keydown', (e) => {
    if (modal.classList.contains('hidden')) return;
    if (e.key === 'Escape') closeModal();
    if (e.key === 'ArrowLeft') showPrev();
    if (e.key === 'ArrowRight') showNext();
});
