// Définir la fonction pour reformater la date
function formatDate(dateStr) {
    // Vérifie que la chaîne de date a bien 6 caractères et est numérique
    if (dateStr.length !== 6 || isNaN(dateStr)) {
        console.log('Date invalide : mauvaise longueur ou non numérique');
        return 'Date invalide';
    }

    // Extraire le jour, le mois et l'année
    const day = dateStr.substring(0, 2);
    const month = dateStr.substring(2, 4);
    const year = dateStr.substring(4, 6);

    // Vérifier que les composantes sont valides
    if (day < 1 || day > 31 || month < 1 || month > 12 || year < 0 || year > 99) {
        console.log('Date invalide : composantes incorrectes');
        return 'Date invalide';
    }

    // Convertir l'année en format complet
    const fullYear = `${year}`;

    // Formater la date en DD/MM/YYYY
    return `${day.padStart(2, '0')}-${month.padStart(2, '0')}-${fullYear}`;
}

