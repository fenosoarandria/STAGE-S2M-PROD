function showAlert(message, type) {
    const alertContainer = document.querySelector('.alert-container');
    if (alertContainer) {
        console.log('Alert container found.');

        // Créer un nouvel élément d'alerte
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-show`;
        alertDiv.innerHTML = `
            <span class="alert-icon">${type === 'success' ? '✓' : '✗'}</span>
            <span class="alert-message">${message}</span>
            <span class="alert-close" onclick="this.parentElement.remove()">×</span>
        `;
        
        // Ajouter l'alerte au conteneur
        alertContainer.appendChild(alertDiv);
        
        // Optionnel : Masquer l'alerte après un certain temps
        setTimeout(() => {
            alertDiv.classList.remove('alert-show');
            alertDiv.style.opacity = '0';
            alertDiv.style.transform = 'translateY(20px)';
            setTimeout(() => {
                alertDiv.remove();
            }, 500); // Attendre que l'animation se termine avant de retirer l'élément
        }, 3000); // Masquer après 3 secondes

    } else {
        console.error('Alert container not found.');
    }
}
