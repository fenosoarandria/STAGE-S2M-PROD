document.addEventListener('DOMContentLoaded', function() {
    UpdateEnseigne();
    UpdateZone();
    RattachementConcurrentDansS2M();
});
function UpdateEnseigne() {
    $(document).ready(function() {
        let enseigneId;
        
        // Lorsqu'un bouton de mise à jour est cliqué
        $('#table-enseigne').on('click', 'button[data-target="#actionEnseigneModal"]', function() {
            enseigneId = $(this).data('id');
            const enseigneName = $(this).data('name');
            const rubrique = $(this).data('rubrique');
            $('#nomEnseigneUpdate').val(enseigneName);
            $('#Rubrique').val(rubrique);
            $('#enseigneId').val(enseigneId);
            document.querySelector('#actionEnseigneModal #nomEnseigneUpdate').value = enseigneName;
            document.querySelector('#actionEnseigneModal #Rubrique').value = rubrique;
            document.querySelector('#actionEnseigneModal #enseigneId').value = enseigneId;
        });
        
        // Lorsqu'un formulaire est soumis
        $('#updateEnseigneForm').off('submit').on('submit', function(event) {
            event.preventDefault();

            if (!enseigneId) {
                console.error('Aucun ID spécifié pour la mise à jour.');
                return;
            }

            const formData = new FormData(this);
            fetch(`/releveprix/update-enseigne/${enseigneId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': $(this).find('[name="csrfmiddlewaretoken"]').val()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Enseigne(); // Recharger les données après mise à jour
                    $('#actionEnseigneModal').modal('hide');
                    setTimeout(() => {
                        showAlert(data.message, 'success');
                    }, 100);
             
                } else {
                    setTimeout(() => {
                        showAlert(data.message, 'danger');
                    }, 100);
             
                }
            })
            .catch(error => {
                setTimeout(() => {
                    showAlert('Une erreur est survenue.', 'danger');
                }, 100);
                console.error('Erreur de fetch:', error);
            });
        });
    });
}

function UpdateZone() {
    $(document).ready(function() {
        let zoneId;

        // Lorsqu'un bouton de mise à jour est cliqué
        $('#table-zone').on('click', 'button[data-target="#actionZoneModal"]', function() {
            zoneId = $(this).data('id');
            const villeName = $(this).data('ville');
            const zoneName = $(this).data('zone');
            
            $('#ville').val(villeName);
            $('#zone').val(zoneName);
            $('#zoneId').val(zoneId);

            document.querySelector('#actionZoneModal #ville').value = villeName;
            document.querySelector('#actionZoneModal #zone').value = zoneName;
            document.querySelector('#actionZoneModal #zoneId').value = zoneId;
        });

        // Lorsqu'un formulaire est soumis
        $('#updateZoneForm').off('submit').on('submit', function(event) {
            event.preventDefault();

            if (!zoneId) {
                console.error('Aucun ID spécifié pour la mise à jour.');
                return;
            }

            const formData = new FormData(this);
            fetch(`/releveprix/update-zone/${zoneId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': $(this).find('[name="csrfmiddlewaretoken"]').val()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Zone(); // Recharger les données après mise à jour
                    $('#actionZoneModal').modal('hide');
                    setTimeout(() => {
                        showAlert(data.message, 'success');
                    }, 100);
             
                } else {
                    setTimeout(() => {
                        showAlert(data.message, 'danger');
                    }, 100);
                }
            })
            .catch(error => {
                setTimeout(() => {
                    showAlert('Une erreur est survenue.', 'danger');
                }, 100);
                console.error('Erreur de fetch:', error);
            });
        });
    });
}

function ReinitialiseEtatReleve(event, button) {
    // Empêcher le comportement par défaut du bouton (affichage automatique du modal)
    event.preventDefault();

    // Récupérer les éléments du modal
    const numeroId = document.getElementById('num');
    const nomId = document.getElementById('nom');
    const enseigneId = document.getElementById('enseignes');
    const hiddenNumInput = document.getElementById('hiddenNum');
    const hiddenEtatInput = document.getElementById('hiddenEtat');


    // Récupérer les attributs du bouton
    const numero = button.getAttribute('data-numero');
    const nom = button.getAttribute('data-nom');
    const enseigne = button.getAttribute('data-enseigne');
    const etat = button.getAttribute('data-etat');


    // Mettre à jour le contenu du modal
    numeroId.innerHTML = numero ? numero : 'Non disponible';
    nomId.innerHTML = nom ? nom : 'Non disponible';
    enseigneId.innerHTML = enseigne ? enseigne : 'Non disponible';
    hiddenNumInput.value = numero;
    hiddenEtatInput.value = etat;


    // Vérifier les conditions d'erreur
    if (etat == 0) {
        showAlert('ERREUR: Téléchargement déjà disponible!.', 'danger');
        console.log('Condition d\'erreur 0 remplie. Modal ne sera pas affiché.');
        return; // Ne pas afficher le modal
    }
    else if (etat == 1) {
            showAlert('ERREUR: Impossible de réinitialiser ce relevé car il est déjà transferé via VARIKA', 'danger');
            console.log('Condition d\'erreur 3 remplie. Modal ne sera pas affiché.');
            return; // Ne pas afficher le modal
    }
    else if (etat == 2) {
        showAlert('ERREUR: Impossible de réinitialiser ce relevé car il est déjà validé', 'danger');
        console.log('Condition d\'erreur 3 remplie. Modal ne sera pas affiché.');
        return; // Ne pas afficher le modal
    } 
    else{
        $('#reinitialisationReleveModal').modal('show'); // Afficher le modal en utilisant jQuery
    }

}

function ConfirmUpdateEtatReleve() {
    const numero = document.getElementById('hiddenNum').value;
    const etat = document.getElementById('hiddenEtat').value;
    
    fetch('/releveprix/update-etat-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'num': numero,
            'etat':etat
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            // Réinitialiser les données et mettre à jour la vue
            applyFiltersReleveIndex();
            const paginationReleve = paginateTable('table-releve', 'pagination-releve', 5);
            setupSearch('searchReleveInput', 'table-releve', paginationReleve);
            // Fermer le modal après un succès
            $('#reinitialisationReleveModal').modal('hide');
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Erreur lors de la mise à jour.', 'danger');
    });
}

function UpdateInformationArticleConcurrent() {
        
    const ref = document.getElementById('s2mReference').value;
    const libelle = document.getElementById('concurrentLibelle').value;
    const gencode = document.getElementById('concurrentGencode').value;
    const prix = document.getElementById('concurrentPrix').value;
    const autre = document.getElementById('concurrentAutre').value;
    const id = document.getElementById('releveNumberInput').value;
    
    fetch('/releveprix/update-information-article-concurrent/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'ref': ref,
            'libelle': libelle,
            'gencode': gencode,
            'prix': prix,
            'autre': autre
        })
    })
    .then(response => {
        console.log('Server Response:', response);  // Ajouter cette ligne pour vérifier la réponse du serveur
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            DetailReleve(id);
            // Réinitialiser les données et mettre à jour la vue
            const paginationDetail = paginateTable('table-detail-releve', 'pagination-detail-releve', 5);
            setupSearch('searchDetailReleveInput', 'table-detail-releve', paginationDetail);
            // Fermer le modal après un succès
            $('#modifierDetailReleveModal').modal('hide');
            $('#detailReleveModal').modal('show');
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Fetch Error:', error);  // Ajouter cette ligne pour vérifier les erreurs de fetch
        showAlert('Erreur lors de la mise à jour.', 'danger');
    });
}    

function ValidationReleve() {
    const numero_releve = sessionStorage.getItem('num_releve');
    console.log(numero_releve)
    fetch('/releveprix/validation-etat-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'num_rel_rel': numero_releve
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            $('#detailReleveModal').modal('hide');
            applyFiltersReleveIndex();
            // Réinitialiser les données et mettre à jour la vue
        }
    })
    .catch(error => {
        showAlert('Erreur lors de la mise à jour.', 'danger');
    });
}

function RattachementConcurrentDansS2M() {
    $(document).ready(function() {
        let concurrentId;

        // Lorsqu'un bouton de rattachement est cliqué
        $('#table-article-concurrent').on('click', 'button[data-target="#rattachementS2mModal"]', function() {
            // Récupérer l'ID du concurrent à partir de l'attribut data-id_concur
            concurrentId = $(this).data('id_concur');

            // Assigner l'ID au champ caché dans le modal
            $('#idConcurrent').val(concurrentId);
        });

        // Lorsqu'on clique sur le bouton "Rattacher" dans le modal
        $('#rattachButton').on('click', function(event) {
            event.preventDefault(); // Empêche le comportement par défaut

            // Récupère la référence saisie dans le champ de texte
            const ref = $('#reference_s2m').val();
            
            // Vérifie si l'ID du concurrent est bien défini
            if (!concurrentId) {
                console.error('ID concurrent non trouvé.');
                showAlert('L\'ID du concurrent n\'a pas été trouvé.', 'danger');
                return;
            }

           
            console.log('Référence S2M:', ref);
            console.log('ID Concurrent récupéré:', concurrentId); // Vérification dans la console


            // Envoie la requête via fetch
            fetch(`/releveprix/rattachement-article-s2m/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    'id_art_concur': concurrentId,
                    'reference_s2m': ref
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    applyFiltersArticleConcurrent();
                    showAlert(data.message, 'success');
                    $('#rattachementS2mModal').modal('hide'); // Ferme le modal après succès
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Erreur lors du rattachement:', error);
                showAlert('Une erreur est survenue lors du rattachement.', 'danger');
            });
        });
    });
}
