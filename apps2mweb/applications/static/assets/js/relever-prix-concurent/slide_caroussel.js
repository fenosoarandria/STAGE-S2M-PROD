function showSlide(index) {
    const slides = document.querySelectorAll('.slide_releve');
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) {
            slide.classList.add('active');
        }
    });

    // Ajuster la position du carrousel
    const carouselImages = document.querySelector('.carousel-images');
    const offset = index * -100; // Calculer le décalage
    carouselImages.style.transform = `translateX(${offset}%)`; // Déplacer le carrousel
}

function nextSlide() {
    const slides = document.querySelectorAll('.slide_releve');
    currentSlide = (currentSlide + 1) % slides.length; // Passer à l'image suivante
    showSlide(currentSlide);
}

function prevSlide() {
    const slides = document.querySelectorAll('.slide_releve');
    currentSlide = (currentSlide - 1 + slides.length) % slides.length; // Passer à l'image précédente
    showSlide(currentSlide);
}
