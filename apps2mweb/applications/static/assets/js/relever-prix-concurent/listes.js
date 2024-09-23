document.addEventListener('DOMContentLoaded', function() {
    Enseigne();
    Zone();
});
let filteredDataEnseigne=[]
let filteredDataZone=[]
let filteredDataReleveArticle=[]
let filteredDataReleveArticleRattache=[]


function Enseigne() {
    fetch('/releveprix/liste-enseigne/')
        .then(response => response.json())
        .then(data => {
            filteredDataEnseigne = data.data;
            const tableBody = document.querySelector('#table-enseigne tbody');

            if (!tableBody) {
                return;
            }

            tableBody.innerHTML = '';

            data.data.forEach(item => {
                const row = document.createElement('tr');

                // Définir l'URL en fonction de l'ID
                let enseigneLink;
                switch (String(item.enseigne_ens)) {
                    case '1':
                        enseigneLink = `<a href="http://www.leaderprice.mg/" target="_blank">${item.libelle_ens}</a>`;
                        break;
                    case '2':
                        enseigneLink = `<a href="https://www.lineaires.com/les-produits" target="_blank">${item.libelle_ens}</a>`;
                        break;
                    case '3':
                        enseigneLink = `<a href="https://vymaps.com/MG/Shop-Liantsoa-27826/" target="_blank">${item.libelle_ens}</a>`;
                        break;
                    case '4':
                        enseigneLink = `<a href="https://www.kibo.mg/" target="_blank">${item.libelle_ens}</a>`;
                        break;
                    default:
                        enseigneLink = `${item.libelle_ens}`; // Utiliser un texte simple si aucune condition n'est remplie
                }

                row.innerHTML = `
                    <td>${item.enseigne_ens}</td>
                    <td>${enseigneLink}</td>
                    <td>${item.lib_plus_ens}</td>
                    <td>
                        <button class="btn btn-secondary btn-sm" id="btn-update" 
                            data-toggle="modal" data-target="#actionEnseigneModal" 
                            data-id="${item.enseigne_ens}" data-name="${item.libelle_ens}" 
                            data-rubrique="${item.lib_plus_ens}" 
                            data-toggle="tooltip" data-placement="top" title="Edit enseigne" >
                        <i class="flaticon-edit"></i>
                    </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            if (data.data.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="4">Aucune donnée disponible</td>';
                tableBody.appendChild(row);
            }

            // Configure pagination
            const paginationEnseigne = paginateTable('table-enseigne', 'pagination-enseigne', 5);
            setupSearch('searchEnseigneInput', 'table-enseigne', paginationEnseigne);
        })
        .catch(error => console.error('Error:', error));
}

function Zone() {
    fetch('/releveprix/liste-zone/')
        .then(response => response.json())
        .then(data => {
            filteredDataZone = data.data;
            const tableBody = document.querySelector('#table-zone tbody');
            
            if (!tableBody) {
                // console.error('Table body element not found.');
                return;
            }
            
            tableBody.innerHTML = ''; // Nettoyer le tableau existant
            
            data.data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.zone_zn}</td>
                    <td>${item.libelle_zn}</td>
                    <td>${item.lib_plus_zn}</td>
                    <td>
                        <button class="btn btn-secondary btn-sm" data-toggle="modal" data-target="#actionZoneModal" 
                                data-id="${item.zone_zn}" data-ville="${item.libelle_zn}" 
                                data-zone="${item.lib_plus_zn}" 
                                data-toggle="tooltip" data-placement="top" title="Edit zone">
                            <i class="flaticon-edit"></i>
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            if (data.data.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="4">Aucune donnée disponible</td>';
                tableBody.appendChild(row);
            }
            
            // Configure pagination
            const paginationZone = paginateTable('table-zone', 'pagination-zone', 5);
            setupSearch('searchZoneInput', 'table-zone', paginationZone);
        })
        .catch(error => console.error('Error:', error));
}

function Releve() {
    fetch('/releveprix/liste-releve/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#table-modal-import-releve tbody');
            
            if (!tableBody) {
                // console.error('Table body element not found.');
                return;
            }
            
            tableBody.innerHTML = ''; // Nettoyer le tableau existant
            data.data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${ item.id_releve }</td>
                    <td>${ item.libelle_releve }</td>
                    <td>${ item.libelle_ens }</td>
                    <td>${ item.date_releve }</td>
                    <td>
                        <input type="checkbox"> 
                    </td>
                `;
                tableBody.appendChild(row);
            });

            if (data.data.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="4">Aucune donnée disponible</td>';
                tableBody.appendChild(row);
            }
            
            // Configure pagination
            const paginationReleve = paginateTable('table-modal-import-releve', 'pagination-modal-import-releve', 5);
            setupSearch('searchImportInput', 'table-modal-import-releve', paginationReleve);
        })
        .catch(error => console.error('Error:', error));
}

function IndexReleveById(itemId){
    const lib = document.getElementById('libelle');
    if (lib) {  // Vérification que l'élément existe
        fetch('/releveprix/releve-index/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Ajout du token CSRF
            },
            body: new URLSearchParams({ id_releve: itemId })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP ! Statut : ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data.data.forEach(item => {
                // sessionStorage.setItem('zone_prix', item.zone_releve);
                document.querySelector('#nouveauArticleModal #id_zone').value = item.zone_releve;
                document.querySelector('#nouveauArticleModal #id_enseigne').value = item.enseigne_releve;
                document.querySelector('#nouveauArticleConcurrentModal #id_zone').value = item.zone_releve;
                document.querySelector('#nouveauArticleConcurrentModal #id_enseigne').value = item.enseigne_releve;

                lib.innerHTML = `RELEVE: ${item.libelle_releve}<p>N°:${item.id_releve} du ${item.date_releve}</p>`;
                if(item.etat_rel == 1){
                    
                    $('#validationreleve').show();
                    $('#import_releve').hide();
                    $('#import_conc').hide();
                    $('#modifier_releve').show();    
                }
                else if(item.etat_rel == 0 || item.etat_rel == 4){
                    $('#import_releve').show();
                    $('#import_conc').show();
                    $('#validationreleve').hide();
                    $('#modifier_releve').show();    
                }else if(item.etat_rel == 2 ){
                    $('#import_releve').hide();
                    $('#import_conc').hide();
                    $('#validationreleve').hide(); 
                    $('#modifier_releve').hide();    
                }else if(item.etat_rel == 3){
                    $('#import_releve').hide();
                    $('#import_conc').hide();
                    $('#validationreleve').hide();  
                    $('#modifier_releve').show();    
                }
                
            })
        })
        .catch(error => {
            console.error('Erreur lors de la requête fetch:', error);
        });
    }
}

function DetailReleve(itemId) {
    IndexReleveById(itemId);
    
    // Stocker la valeur avec une clé dynamique
    sessionStorage.setItem('num_releve', itemId);
   
    fetch('/releveprix/liste-detail-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        filteredDataReleveArticle = data.data;
        const tableBody = document.querySelector('#table-detail-releve tbody');
        
        if (!tableBody) {
            console.error('Élément table body non trouvé.');
            return;
        }
        
        tableBody.innerHTML = ''; // Nettoyer le tableau existant

        data.data.forEach(item => {
            const prixRef = item.prix_ref_rel != null ? item.prix_ref_rel : '0';
            const prixZone = item.prix_zone_rel != null ? item.prix_zone_rel :'0';
            const prixConcurrent = item.prix_concur_rel != null ? item.prix_concur_rel: '0';


            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <button class="btn-advanced" 
                            onClick="InfoArticleReleve(this)" 
                            data-toggle="modal" 
                            data-target="#modifierDetailReleveModal" 
                            data-ref_rel="${item.ref_rel}" 
                            data-id_rel_rel="${item.id_rel_rel}" 
                            data-num_rel_rel="${item.num_rel_rel}" 
                            data-toggle="tooltip" 
                            data-placement="top" 
                            title="Modifier l'information par article">
                        ${item.ref_rel || 'N/A'}
                    </button>
                </td>
                <td style="color:green;">${item.libelle_art_rel || ''}</td>
                <td style="color:green;">${item.gencod_rel || ''}</td>
                <td style="color:green;">${prixRef}</td>
                <td style="color:green;">${prixZone}</td>
                <td>${item.lib_art_concur_rel || ''}</td>
                <td>${item.gc_concur_rel|| ''}</td>
                <td>${prixConcurrent}</td>
                <td>${item.lib_plus_rel || ''}</td>
                <td>${item.lib_etat_rel || ''}</td>
                <td>${item.lib_rel_modif || ''}</td>
            `;
            tableBody.appendChild(row);
        });
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="12">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        }
        // Configure pagination
        const paginationDetailReleve = paginateTable('table-detail-releve', 'pagination-detail-releve', 4);
        setupSearch('searchDetailReleveInput', 'table-detail-releve', paginationDetailReleve);

    })
    .catch(error => console.error('Erreur:', error));
}

function InfoArticleReleve(button) {
    const itemRefRel = button.getAttribute('data-ref_rel');
    const itemIdRelRel = button.getAttribute('data-id_rel_rel');
    const itemNumRelRel = button.getAttribute('data-num_rel_rel');
    const concurrent = document.getElementById('concurrent_info');
    sessionStorage.removeItem('num_releve');

    // Effectuer la requête fetch
    fetch(`/releveprix/info-article/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ ref_rel: itemRefRel,id_rel_rel: itemIdRelRel,num_rel_rel:itemNumRelRel})
    })
    .then(response => response.json())
    .then(data => {
        data.data.forEach(row => {
            // Mise à jour des champs dans le modal
            //S2M
            document.querySelector('#modifierDetailReleveModal #id_rel_rel').value = row.id_rel_rel;
            document.querySelector('#modifierDetailReleveModal #dateInput').value = row.date_rel;
            document.querySelector('#modifierDetailReleveModal #releveNumberInput').value = row.num_rel_rel;
            document.querySelector('#modifierDetailReleveModal #s2mReference').value = row.ref_rel;
            document.querySelector('#modifierDetailReleveModal #s2mLibelle').value = row.libelle_art_rel;
            document.querySelector('#modifierDetailReleveModal #s2mGencode').value = row.gencod_rel;
            document.querySelector('#modifierDetailReleveModal #s2mPrix').value = row.prix_ref_rel;
            document.querySelector('#modifierDetailReleveModal #s2mZone').value = row.lib_zn_rel;
            //CONCURRENT
            document.querySelector('#modifierDetailReleveModal #id_concurrent').value = row.id_concurrant;
            document.querySelector('#modifierDetailReleveModal #concurrentReference').value = row.num_rel_rel;
            document.querySelector('#modifierDetailReleveModal #concurrentLibelle').value = row.lib_art_concur_rel;
            document.querySelector('#modifierDetailReleveModal #concurrentGencode').value = row.gc_concur_rel;
            document.querySelector('#modifierDetailReleveModal #concurrentPrix').value = row.prix_concur_rel;
            document.querySelector('#modifierDetailReleveModal #concurrentAutre').value = row.lib_plus_rel;
            concurrent.innerHTML = row.libelle_ens;
            // Trouve l'élément où tu veux insérer l'image
            // Crée l'URL de l'image
            const imageUrl = `/static/img/Nouveau_article/${row.gc_concur_rel}.png`;

            // Trouve l'élément où tu veux insérer l'image
            const conteneur = document.querySelector('#conteneurImage');

            // Insère le code HTML de l'image dans le conteneur
            conteneur.innerHTML = `
                <style>
                    #articlePhoto:hover {
                        transform: scale(1.1);
                    }
                </style>
                <img src="${imageUrl}" 
                    alt="Photo de l'article" 
                    id="articlePhoto" 
                    class="img-fluid" 
                    style="max-width: 100%; transition: transform 0.3s ease-in-out; cursor: pointer;">
            `;



        });
    })
    .catch(error => {
        console.error('Erreur lors de la requête fetch:', error);
    });
}

function RattachementReleve(itemId,s2m) {
    sessionStorage.setItem("reference",itemId)
    sessionStorage.setItem("gencode_s2m",s2m)
    if (!itemId) {
        console.error('L\'ID est undefined, annulation de la requête.');
        return;
    }

    fetch('/releveprix/liste-rattachement-externe-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ ref: itemId })
    })
    .then(response => response.json())
    .then(data => {
        filteredDataReleveArticleRattache = data.data;

        const tableBody = document.querySelector('#table-rattachement-releve-article tbody');
        
        if (!tableBody) {
            console.error('Élément table body non trouvé.');
            return;
        }
        
        tableBody.innerHTML = ''; // Nettoyer le tableau existant

        data.data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ item.id_art_concur }</td>
                <td>${ item.libelle_ens }</td>
                <td>${ item.ref_ac }</td>
                <td>${ item.libelle_ac }</td>
                <td>${ item.gencod_ac }</td>
            `;
            tableBody.appendChild(row);
        });
    
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        }

        // Configure pagination
        const paginationDetailReleve = paginateTable('table-rattachement-releve-article', 'pagination-rattachement-releve-article', 5);
        setupSearch('searchRattachementReleveArticleInput', 'table-rattachement-releve-article', paginationDetailReleve);
    })
    .catch(error => console.error('Erreur:', error));
}


function HistoriqueReleve(itemId) {
    if (!itemId) {
        console.error('L\'ID est undefined, annulation de la requête.');
        return;
    }

    fetch('/releveprix/liste-historique-releve/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ ref: itemId })
    })
    .then(response => response.json())
    .then(data => {
        
        const tableBody = document.querySelector('#table-historique-releve-article tbody');
        
        if (!tableBody) {
            console.error('Élément table body non trouvé.');
            return;
        }
        
        tableBody.innerHTML = ''; // Nettoyer le tableau existant
        const validation = '';
        data.data.forEach(item => {
            console.log(data)
            // if (item.date_val_releve != null){
            //     validation = item.date_val_releve;
            // }
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ item.date_rel }</td>
                <td>${ item.libelle_ens }</td>
                <td>${ item.prix_ref_rel }</td>
                <td>${ item.prix_concur_rel }</td>
                <td>${ item.date_val_releve }</td>
            `;
            tableBody.appendChild(row);
        });
    
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5">Aucune donnée disponible</td>';
            tableBody.appendChild(row);
        }

        // Configure pagination
        const paginationHistoriqueReleve = paginateTable('table-historique-releve-article', 'pagination-historique-releve-article', 5);
        setupSearch('searchHistoriqueReleveArticleInput', 'table-historique-releve-article', paginationHistoriqueReleve);
    })
    .catch(error => console.error('Erreur:', error));
}


function TypeFiltre(selectedValue) {
    // Récupérer la valeur avec la même clé
    const params = new URLSearchParams({
        nomenclature: selectedValue
    });

    if (!selectedValue) {
        document.getElementById('select-container').innerHTML = '';
        return;
    }

    fetch(`/releveprix/liste-nomenclature/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: params
    })
    .then(response => response.json())
    .then(data => {
        // Assurez-vous que data.data est un tableau
        if (Array.isArray(data.data)) {
            const container = document.getElementById('select-container');
            container.innerHTML = ''; // Vider le conteneur

            let selectHtml = '';
            // Cas spécifique pour 'ray'
            if (selectedValue === 'ray') {
                const options = data.data.map(item => 
                    `<option value="${item.ray_ray}">${item.ray_ray} - ${item.libelle_ray}</option>`
                ).join('');
                selectHtml = `
                    <select id="filtre" class="selectpicker form-control" data-live-search="true">
                        ${options}
                    </select>`;
            } else {
                // Cas pour les autres critères (art, sec, fam, sfam)
                const columnMapping = {
                    'art': { value: 'art'},
                    'sec': { value: 'sec'},
                    'fam': { value: 'fam'},
                    'sfam': { value: 'sfam'}
                };
                // Obtenez les noms de colonnes appropriés en fonction de selectedValue
                const columns = columnMapping[selectedValue];
                if (columns) {
                    const options = data.data.map(item => 
                        `<option value="${item[columns.value]}">${item[columns.value]}</option>`
                    ).join('');
                    selectHtml = `
                        <select id="filtre" class="selectpicker form-control" data-live-search="true"> 
                            ${options}
                        </select>`;
                } else {
                    console.error('Critère non reconnu:', selectedValue);
                }
            }
            
            // Injecter le HTML dans le conteneur
            container.innerHTML = selectHtml;

         
            // Initialiser ou rafraîchir le sélecteur si nécessaire
            $('.selectpicker').selectpicker('refresh');
        } else {
            console.error('Erreur: Les données reçues ne sont pas un tableau.', data);
        }
    })
    .catch(error => console.error('Erreur:', error));
}
