document.addEventListener('DOMContentLoaded', function() {
    applyFiltersReleveIndex();
    applyFiltersRecap(); 
    applyFiltersArticleS2M();
    applyFiltersArticleConcurrent();
});
let filteredDataArticleS2m = []; // Variable globale pour stocker les données filtrées
let filteredDataArticleConcurrent = []; // Variable globale pour stocker les données filtrées
let filteredDataReleve = []; // Variable globale pour stocker les données filtrées
let filteredDataRecap = []; // Variable globale pour stocker les données filtrées


// Fonction pour appliquer les filtres et mettre à jour le tableau des articles S2M
function applyFiltersArticleS2M() {
   
    const formData = new URLSearchParams();

    // Définir les sélecteurs des filtres
    const selecteur = ['fournisseur', 'rayon', 'gencode'];
    if(document.querySelector('[name=csrfmiddlewaretoken]') == null){
        return;
    }
    // Créer les données de formulaire à partir des sélecteurs
    selecteur.forEach(className => {
        const value = $(`#${className}`).val();
        if (value) formData.append(className, value);
    });

    // Afficher le spinner de chargement
    showLoadingSpinner('#loading_article_s2m', true);

    // Envoyer la requête fetch pour obtenir les données filtrées
    fetch('/releveprix/filtre-article-s2m/', {
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
        const tableBody = document.querySelector('#table_article_s2m');
        tableBody.innerHTML = '';
        filteredDataArticleS2m = data.data; // Variable globale pour stocker les données filtrées

        
        // Vérifier si des données sont disponibles
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="10">Aucune donnée disponible</td>';
            // showAlert('Aucune donnée', 'danger');
            tableBody.appendChild(row);
        } else {
            // Remplir le tableau avec les nouvelles données
            data.data.forEach(row => {
                
                const rowHtml = `
                    <tr>
                        <td><button class="btn-advanced" data-toggle="modal" data-target="#historiqueReleveArticleModal" onClick=HistoriqueReleve(${row.art}) data-toggle="tooltip" data-placement="top" title="Historique relevé">${row.art}</button></td>
                        <td>${row.lib}</td>
                        <td>${row.ray}</td>
                        <td>${row.gencod}</td>
                        <td>${row.sec}-${row.ray}-${row.fam}-${row.sfam}</td>
                        <td>${row.fn} - ${row.raison_social_frs}</td>
                        <td>${row.tva_vte}</td>
                        <td>${formatDate(String(row.date_creat))}</td>
                        <td>${formatDate(String(row.date_maj))}</td>
                        <td><button class="btn-advanced" data-toggle="modal" data-target="#rattachementReleveArticleModal" onClick="RattachementReleve(${row.art},${row.gencod})" data-toggle="tooltip" data-placement="top" title="Rattachement relevé">${row.article_rattache}</button></td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', rowHtml);
            });

            // Initialiser la pagination et la recherche
            const paginationArticleS2M = paginateTable('table-article-s2m', 'pagination-article-s2m', 5);
            setupSearch('searchArticleS2mInput', 'table-article-s2m', paginationArticleS2M);
        }
        showLoadingSpinner('#loading_article_s2m', false);
        // Arrêter le spinner après traitement
    })
    .catch(error => console.error('Erreur:', error));
}

function applyFiltersRecap() {
    const formData = new URLSearchParams();

    // Définir les sélecteurs des filtres
    const selecteur = ['date_debut', 'date_fin','ref_rel_recap_gencode'];
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfTokenElement == null) {
        return;
    }
    
    // Créer les données de formulaire à partir des sélecteurs
    selecteur.forEach(className => {
        const value = document.getElementById(className).value;
        if (value) formData.append(className, value);
    });

    showLoadingSpinner('#loading_recap', true);
    // Envoyer la requête fetch pour obtenir les données filtrées
    fetch('/releveprix/filtre-article-recapitulatif/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfTokenElement.value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        filteredDataRecap = data.data;
        const tableBody = document.querySelector('#recapitulatif');
        tableBody.innerHTML = ''; // Vider le tableau avant d'insérer les nouvelles données

        // Vérifier si des données sont disponibles
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="13">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        } else {
            // Insérer les nouvelles lignes de données
            data.data.forEach(row => {
                const rayl30c = row.article_data.ray != null ? row.article_data.ray : '';
                const prixRefRel = row.prix_ref_rel != null ? row.prix_ref_rel.toLocaleString() : 'N/A';
                const prixConcurRel = row.prix_concur_rel != null ? row.prix_concur_rel.toLocaleString() : 'N/A';
                const differencePrix = (row.prix_ref_rel != null && row.prix_concur_rel != null) ?
                    row.prix_ref_rel - row.prix_concur_rel : 'N/A';
                    const ens = row.libelle_ens!= null ? row.libelle_ens:'';

                const rowHtml = `
                    <tr>
                        <td>${row.date_rel}</td>
                        <td>${row.num_rel_rel}</td>
                        <td>${ens}</td>
                        <td>${row.ref_rel}</td>
                        <td>${row.libelle_art_rel}</td>
                        <td>${row.gencod_rel}</td>
                        <td>${rayl30c}</td>
                        <td>${prixRefRel}</td>
                        <td>${row.id_art_conc_rel}</td>
                        <td>${row.gc_concur_rel}</td>
                        <td>${row.lib_art_concur_rel}</td>
                        <td>${prixConcurRel}</td>
                        <td>${differencePrix}</td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', rowHtml);
            });

        }
        // Initialiser la pagination et la recherche
        const paginationRecapitulatif = paginateTable('table-recapitulatif-article', 'pagination-recapitulatif-article', 5);
        setupSearch('searchRecapitulatifArticleInput', 'table-recapitulatif-article', paginationRecapitulatif);
        showLoadingSpinner('#loading_recap', false);

    })
    .catch(error => console.error('Erreur:', error));
}

function applyFiltersReleveIndex() {

    const formData = new URLSearchParams();

    const selecteur = ['date-debut', 'date-fin','concurrent'];
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if(csrfTokenElement == null){
        return;
    }

    selecteur.forEach(className => {
        const value = $(`#${className}`).val();
        if (value) formData.append(className, value);
    });
    showLoadingSpinner('#loading_releve', true);

    fetch('/releveprix/filtre-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfTokenElement.value
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        filteredDataReleve=data.data;
        const tableBody = document.querySelector('#releve');
        tableBody.innerHTML = '';
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="10">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        } else {
            data.data.forEach(row => {
                const rowHtml = `
                    <tr data-id="${row.id_releve}">
                        <td>
                        <button class="btn-advanced" data-toggle="modal" data-target="#detailReleveModal" 
                            data-id="${row.id_releve}"
                            data-toggle="tooltip" data-placement="top" title="Detail relevé" 
                            onClick="DetailReleve('${row.id_releve}')">${row.id_releve}
                        </button></td>
                        <td>${row.libelle_ens}</td>
                        <td>${row.libelle_zn}</td>
                        <td>${row.libelle_releve}</td>
                        <td>${row.date_releve}</td>
                        <td>${row.lib_plus_releve}</td>
                        <td>${row.dt_maj_releve}</td>
                        <td>${row.nb_article}</td>
                        <td>${row.etat_rel} - ${row.lib_etat_rel}</td>
                        <td>
                            <button class="btn-params" onClick="ReinitialiseEtatReleve(event, this)" data-numero="${row.id_releve}" data-nom="${row.libelle_releve}" data-enseigne="${row.libelle_ens}" data-etat="${row.etat_rel}" data-toggle="tooltip" data-placement="top" title="Reinitialiser relevé"><i class="flaticon-gear"></i></button>
                            <button class="btn-delete" data-toggle="modal" data-target="#deleteReleveModal" data-id="${row.id_releve}" data-toggle="tooltip" data-placement="top" title="Supprimer relevé"><i class="flaticon-delete delete-icon"></i></button>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', rowHtml);
            });
            
            
            // Réinitialiser et configurer la pagination et la recherche après le chargement des nouvelles données
            const paginationReleve = paginateTable('table-releve', 'pagination-releve', 5);
            setupSearch('searchInput', 'table-releve', paginationReleve);
            setupDeleteReleve('deleteReleveModal', 'deleteReleve');
        }
        showLoadingSpinner('#loading_releve', false);
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}


function applyFiltersArticleConcurrent() {
    const formData = new URLSearchParams();
    const selecteur = ['ens_id', 'rattachement'];

    if (document.querySelector('[name=csrfmiddlewaretoken]') == null) {
        return;
    }

    selecteur.forEach(className => {
        const value = $(`#${className}`).val();
        if (value) formData.append(className, value);
    });

    showLoadingSpinner('#loading_article_concurrent', true);

    fetch('/releveprix/filtre-article-concurrent/', {
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
            throw new Error(`Erreur réseau: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        const tableBody = document.querySelector('#table_article_concurrent');
        tableBody.innerHTML = '';

        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="6">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        } else {
            data.data.forEach(row => {
                filteredDataArticleConcurrent = data.data;
                const rowHtml = `
                    <tr>
                        <td>${row.libelle_ens}</td>
                        <td>${row.ref_rel}</td>
                        <td>${row.lib_art_concur_rel}</td>
                        <td>${row.gc_concur_rel}</td>
                        <td>${row.prix_concur_rel}</td>
                        <td>
                            <img src="${row.image}" 
                                alt="Photo de l'article" 
                                class="img-article" 
                                style="width: 100px; cursor: pointer;" 
                                onclick="openImageModal('${row.image}', '${row.lib_art_concur_rel}')">
                        </td>
                        <td>
                            ${row.statut_rattachement == 1 
                                ? '<span class="statut-coché">Déjà rattaché</span>' 
                                : `<button class="btn-advanced" data-toggle="modal" data-target="#rattachementS2mModal" data-id_concur="${row.id_art_concur}" data-placement="top" title="Rattachement relevé">Rattacher</button>`
                            }
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', rowHtml);
            });
        }

        const paginationArticleConcurrent = paginateTable('table-article-concurrent', 'pagination-table-article-concurrent', 5);
        setupSearch('searchArticleConcurrent', 'table-article-concurrent', paginationArticleConcurrent);
        showLoadingSpinner('#loading_article_concurrent', false);
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des données:', error.message);
        // showLoadingSpinner('#loading_article_concurrent', false);
    });
}

function openImageModal(imageUrl, lib) {
    document.getElementById('modalImage').src = imageUrl;
    document.querySelector('#imageModal #libelle_image').innerHTML = lib;
    $('#imageModal').modal('show');
}
