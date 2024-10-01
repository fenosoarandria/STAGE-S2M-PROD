function InsertReleve() {
    // Récupérer les valeurs des champs du formulaire
    var dateInsertion = document.getElementById('dateInsertion').value;
    var enseigne = document.getElementById('enseigne').value;
    var zone = document.getElementById('zone').value;
    var nomReleve = document.getElementById('nomReleve').value;
    var autreInfo = document.getElementById('autreInfo').value;

    // Vérifier si les champs requis sont remplis
    if (!dateInsertion) {
        showAlert('La date d\'insertion est requise.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }
    if (!enseigne) {
        showAlert('Veuillez sélectionner une enseigne.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }
    if (!zone) {
        showAlert('Veuillez sélectionner une zone.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }
    if (!nomReleve) {
        showAlert('Le nom du relevé est requis.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }

    // Créer un objet avec les données à envoyer
    var formData = new URLSearchParams();
    formData.append('date_creation', dateInsertion);
    formData.append('enseigne', enseigne);
    formData.append('zone', zone);
    formData.append('nom_releve', nomReleve);
    formData.append('autre_info', autreInfo);

    // Envoyer les données via fetch
    fetch('/releveprix/ajout-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Relevé ajouté avec succès', 'success');
            $('#nouveauReleveModal').modal('hide');
            applyFiltersReleveIndex();
            // Rafraîchir la table ou effectuer d'autres actions nécessaires
        } else {
            showAlert('Une erreur est survenue lors de l\'ajout du relevé.', 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showAlert('Une erreur est survenue.', 'danger');
    });
}

function InsertEnseigne() {
    // Récupérer les valeurs des champs du formulaire
    var nomEnseigne = document.getElementById('nomEnseigne').value;
    var rubriqueEnseigne = document.getElementById('rubriqueEnseigne').value;

    // Vérifier si les champs requis sont remplis
    if (!nomEnseigne) {
        showAlert('Le nom de l\'enseigne est requis.', 'danger');
        return;
    }
    if (!rubriqueEnseigne) {
        showAlert('La rubrique est requise.', 'danger');
        return;
    }

    // Créer un objet avec les données à envoyer
    var formData = new URLSearchParams();
    formData.append('nom', nomEnseigne);
    formData.append('rubrique', rubriqueEnseigne);

    // Envoyer les données via fetch
    fetch('/releveprix/ajout-enseigne/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Nouvelle enseigne ajoutée avec succès', 'success');
            $('#nouveauEnseigneModal').modal('hide');
            Enseigne();
            // Rafraîchir la table ou effectuer d'autres actions nécessaires
        } else {
            showAlert('Une erreur est survenue lors de l\'ajout de l\'enseigne.', 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showAlert('Une erreur est survenue.', 'danger');
    });
}

function InsertZone() {
    // Récupérer les valeurs des champs du formulaire
    var ville = document.querySelector('input[name="ville"]').value;
    var zone = document.querySelector('input[name="zone"]').value;

    // Vérifier si les champs requis sont remplis
    if (!ville) {
        showAlert('Le nom de la zone est requis.', 'danger');
        return;
    }
    if (!zone) {
        showAlert('La rubrique est requise.', 'danger');
        return;
    }

    // Créer un objet avec les données à envoyer
    var formData = new URLSearchParams();
    formData.append('ville', ville);
    formData.append('zone', zone);

    // Envoyer les données via fetch
    fetch('/releveprix/ajout-zone/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Zone ajoutée avec succès', 'success');
            $('#nouveauZoneModal').modal('hide');
            Zone();
            // Rafraîchir la table ou effectuer d'autres actions nécessaires
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showAlert('Une erreur est survenue.', 'danger');
    });
}

function InsertNouveauRattachement() {
    var libelle = document.getElementById('libelleArticle').value;
    var gencode = document.getElementById('genCode').value;
    var enseigne = document.getElementById('enseigne_id').value;
    if (!enseigne) {
        showAlert('Veuillez sélectionner une enseigne.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }
    if (!libelle) {
        showAlert('Veuillez saisir une designation.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }
    if (!gencode) {
        showAlert('Gencode requis.', 'danger');
        return; // Arrêter l'exécution de la fonction
    }

    var formData = new URLSearchParams();
    formData.append('enseigne', enseigne); // Utilisation de la valeur sélectionnée
    formData.append('libelle', libelle);
    formData.append('gencode', gencode);
    formData.append('reference', sessionStorage.getItem("reference"));
    formData.append('gencode_s2m', sessionStorage.getItem("gencode_s2m"));

    fetch('/releveprix/ajout-rattachement-article-concurrent/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur réseau');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showAlert('Article rattaché avec succès', 'success');
            RattachementReleve(sessionStorage.getItem("reference"))
            applyFiltersArticleS2M()
            $('#nouveauArticleRattacheModal').modal('hide');
        } else {
            showAlert('Une erreur est survenue lors de rattachement d\'un article.', 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        showAlert('Une erreur est survenue.', 'danger');
    });
}


function InsertArticleReleve() {
    const filtre = document.getElementById('filtre')?.value;
    const critere = document.getElementById('crit')?.value;
    const zone = document.getElementById('id_zone').value;
    const enseigne = document.getElementById('id_enseigne').value;
    const num_releve = sessionStorage.getItem('num_releve');

    if (!filtre) {
        showAlert('Veuillez choisir une critere', 'danger');
        return;
    }

    showLoading();

    const zoneMagMap = {
        'TANANARIVE': 712, 'TANA': 712, 'ANTANANARIVO': 712,
        'TAMATAVE': 713, 'TAMATAVY': 713,
        'MAHAJUNGA': 715, 'MAHAJANGA': 715,
        'DIEGO': 717, 'ANTSIRANANA': 717,
        'TULEAR': 719, 'TOLIARA': 719,
        'FIANARANTSOA': 726
    };
    const mag = zoneMagMap[zone] || 712;

    const formData = new URLSearchParams({
        critere, filtre, mag, num_releve, zone, enseigne
    });

    fetch('/releveprix/ajout-article/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.ok ? response.json() : Promise.reject('Erreur réseau'))
    .then(data => {
        if(data.success){
            showAlert(data.message, 'success');
            $('#nouveauArticleModal').modal('hide');
            DetailReleve(num_releve);
            applyFiltersReleveIndex();
            hideLoading();
        }else{
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        hideLoading();
        showAlert('Une erreur est survenue.', 'danger');
    });
}

