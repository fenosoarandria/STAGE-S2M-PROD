function showLoading() {
    const loadingElement = document.getElementById('loading-indicator');
    if (loadingElement) {
        loadingElement.style.display = 'flex';
    } else {
        // console.error('Loading indicator not found.');
        return;
    }
}

function hideLoading() {
    const loadingElement = document.getElementById('loading-indicator');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    } else {
        // console.error('Loading indicator not found.');
        return;
    }
}


// Fonction pour gérer l'affichage et la suppression de l'animation de chargement
function showLoadingSpinner(selector, show) {
    const spinners = document.querySelectorAll(selector);
    spinners.forEach(spinner => {
        spinner.style.display = show ? "flex" : "none";
    });
}

// Ajoute un événement de clic pour tous les boutons ayant la classe 'loadButton'
document.querySelectorAll(".loading-spinner").forEach(button => {
    button.addEventListener("click", function() {
        const url = this.getAttribute("data-spinner");  // Récupère l'URL à partir de l'attribut data-url
        loadData(url);  // Charge les données pour l'URL correspondante
    });
});

// ... effectuer une tâche asynchrone comme une requête fetch
hideLoading(); // Masquer l'indicateur lorsque la tâche est terminée
