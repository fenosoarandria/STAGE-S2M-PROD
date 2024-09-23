// Fonction pour préparer les données et créer une feuille Excel
function createExcelSheet(data, sheetName, fileName) {
    if (data.length === 0) {
        showAlert('Aucune donnée à exporter.', 'danger');
        return;
    }

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, sheetName);
    
    // const today = new Date();
    // const formattedDateTime = today.toISOString().replace(/[:T]/g, '-').split('.')[0];
    const fullFileName = `${fileName}.xlsx`;

    XLSX.writeFile(wb, fullFileName);
}

// Fonction pour préparer les données pour l'exportation avec des colonnes spécifiques
function prepareDataForExport(data, columns) {
    return data.map(row => {
        const result = {};
        columns.forEach(col => {
            result[col.header] = row[col.key];
        });
        return result;
    });
}

// Fonction d'exportation pour les données de Relevé
function exportListeReleve() {
    const columns = [
        { header: 'ID Relevé', key: 'id_releve' },
        { header: 'Libellé Enseigne', key: 'libelle_ens' },
        { header: 'Libellé Zone', key: 'libelle_zn' },
        { header: 'Libellé Relevé', key: 'libelle_releve' },
        { header: 'Date Relevé', key: 'date_releve' },
        { header: 'Lib Plus Relevé', key: 'lib_plus_releve' },
        { header: 'Date Maj Relevé', key: 'dt_maj_releve' },
        { header: 'Nombre d\'Articles', key: 'nb_article' },
        { header: 'État Relevé', key: 'etat_rel' }
    ];
    const preparedData = prepareDataForExport(filteredDataReleve, columns);
    createExcelSheet(preparedData, 'Relevés', 'Releves');
}

// Répéter le même modèle pour d'autres fonctions d'exportation

function exportArticleS2m() {
    const columns = [
        { header: 'ID', key: 'art' },
        { header: 'Libellé', key: 'lib' },
        { header: 'Rayon', key: 'ray' },
        { header: 'GenCode', key: 'gencod' },
        { header: 'Nomenclature', key: 'nomenclature' },
        { header: 'Fournisseur', key: 'fournisseur' },
        { header: 'TVA', key: 'tva_vte' },
        { header: 'Date Création', key: 'date_creat' },
        { header: 'Date Maj', key: 'date_maj' },
        { header: 'Article Rattaché', key: 'article_rattache' }
    ];
    const preparedData = prepareDataForExport(filteredDataArticleS2m, columns);
    createExcelSheet(preparedData, 'Articles S2M', 'Articles_S2M');
}

function exportArticleConcurrent() {
    
    const columns = [
        { header: 'Enseigne', key: 'enseigne_ac' },
        { header: 'Reference S2M', key: 'ref_rel' },
        { header: 'Libellé article concurrent', key: 'lib_art_concur_rel' },
        { header: 'Gencode concurrent', key: 'gc_concur_rel' },
        { header: 'Prix concurrent', key: 'prix_concur_rel' },
        { header: 'Etat', key: 'statut_rattachement' }
    ];
    const preparedData = prepareDataForExport(filteredDataArticleConcurrent, columns);
    createExcelSheet(preparedData, 'Articles Concurrent', 'Articles_Concurrent');
}

function exportEnseigne() {
    const columns = [
        { header: 'Enseigne ID', key: 'enseigne_ens' },
        { header: 'Libellé', key: 'libelle_ens' },
        { header: 'Lib Plus', key: 'lib_plus_ens' }
    ];
    const preparedData = prepareDataForExport(filteredDataEnseigne, columns);
    createExcelSheet(preparedData, 'Enseignes', 'Enseignes');
}

function exportZone() {
    const columns = [
        { header: 'Zone ID', key: 'zone_zn' },
        { header: 'Libellé', key: 'libelle_zn' },
        { header: 'Lib Plus', key: 'lib_plus_zn' }
    ];
    const preparedData = prepareDataForExport(filteredDataZone, columns);
    createExcelSheet(preparedData, 'Zones', 'Zones');
}

function exportRecap() {
    const columns = [
        { header: 'Date', key: 'date_rel' },
        { header: 'Num Rel', key: 'num_rel_rel' },
        { header: 'Enseigne', key: 'libelle_ens' },
        { header: 'Réf Rel', key: 'ref_rel' },
        { header: 'Libellé Art', key: 'libelle_art_rel' },
        { header: 'Gencode', key: 'gencod_rel' },
        { header: 'Rayon', key: 'ray' },
        { header: 'Prix Ref', key: 'prix_ref_rel' },
        { header: 'ID Art Concurrent', key: 'id_art_conc_rel' },
        { header: 'Gencode Concurrent', key: 'gc_concur_rel' },
        { header: 'Lib Art Concurrent', key: 'lib_art_concur_rel' },
        { header: 'Prix Concurrent', key: 'prix_concur_rel' },
        { header: 'Ecart', key: 'ecart' }
    ];
    const preparedData = prepareDataForExport(filteredDataRecap, columns);
    createExcelSheet(preparedData, 'Export Data', 'Recapitulation');
}

function exportSelectedReleve() {
    const tableBody = document.querySelector('#table-modal-import-releve tbody');
    if (!tableBody) {
        showAlert('Tableau non trouvé.', 'danger');
        return;
    }

    const selectedRows = Array.from(tableBody.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => {
        const row = checkbox.closest('tr');
        return {
            id_releve: row.cells[0].textContent,
            libelle_releve: row.cells[1].textContent,
            libelle_ens: row.cells[2].textContent,
            date_releve: row.cells[3].textContent
        };
    });

    if (selectedRows.length === 0) {
        showAlert('Aucune ligne sélectionnée.', 'danger');
        return;
    }

    const columns = [
        { header: 'ID Relevé', key: 'id_releve' },
        { header: 'Libellé Relevé', key: 'libelle_releve' },
        { header: 'Enseigne', key: 'libelle_ens' },
        { header: 'Date Relevé', key: 'date_releve' }
    ];
    const preparedData = prepareDataForExport(selectedRows, columns);
    createExcelSheet(preparedData, 'Relevés Sélectionnés', 'Releves_Selected');
}

function exportArticleReleve() {
    const columns = [
        { header: 'Référence article S2M', key: 'ref_rel' },
        { header: 'Libellé S2M', key: 'libelle_art_rel' },
        { header: 'Gencode S2M', key: 'gencod_rel' },
        { header: 'Prix référence', key: 'prix_ref_rel' },
        { header: 'Prix Zone', key: 'prix_zone_rel' },
        { header: 'Libellé concurrent', key: 'lib_art_concur_rel' },
        { header: 'Gencode concurrent', key: 'gc_concur_rel' },
        { header: 'Prix Concurrent', key: 'prix_concur_rel' },
        { header: 'Commentaire', key: 'lib_plus_rel' },
        { header: 'Etat relevé', key: 'lib_etat_rel' },
        { header: 'Etat article', key: 'lib_rel_modif' }
    ];
    const preparedData = prepareDataForExport(filteredDataReleveArticle, columns);
    createExcelSheet(preparedData, 'Articles Relevés', 'BLS 2080');
}

function exportArticleExterneRattache() {
    const columns = [
        { header: 'ID', key: 'id_art_concur' },
        { header: 'ENSEIGNE', key: 'libelle_ens' },
        { header: 'REFERENCE', key: 'ref_ac' },
        { header: 'LIBELLE', key: 'libelle_ac' },
        { header: 'GENCODE', key: 'gencod_ac' }
    ];
    const preparedData = prepareDataForExport(filteredDataReleveArticleRattache, columns);
    createExcelSheet(preparedData, 'Articles Rattaché', 'Articles_Rattaché');
}

// ------------------------------------------------------------------------------------------------------------------

// Fonction utilitaire pour gérer les réponses
function handleResponse(response, fileName) {
    if (response.headers.get('content-type').includes('application/json')) {
        return response.json().then(data => {
            if (data.error) {
                showAlert(data.error, 'danger');
            } else {
                showAlert('Erreur lors de la génération du PDF.', 'danger');
            }
        });
    } else if (response.headers.get('content-type').includes('application/pdf')) {
        return response.blob().then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url); // Nettoyer l'URL après le téléchargement
        });
    } else {
        throw new Error('Type de contenu inattendu');
    }
}

// Fonction utilitaire pour envoyer la requête de génération de PDF
function generatePdf(url, fileName, formData) {   
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => handleResponse(response, fileName))
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de la génération du PDF.');
    });
}

// Fonction pour générer le PDF pour le filtre S2M
function generatePdfFiltreS2m() {
    const params = new URLSearchParams({
        fournisseur: document.getElementById('fournisseur').value,
        rayon: document.getElementById('rayon').value,
        gencode: document.getElementById('gencode').value
    }).toString();
    generatePdf('/releveprix/pdf-filtre-article-s2m/', 'rapport_articles_s2m.pdf', params);
}

// Fonction pour générer le PDF pour le filtre Concurrent
function generatePdfFiltreConcurrent() {
    const selecteur = ['ens_id', 'rattachement'];
    const formData = new URLSearchParams();
    selecteur.forEach(id => {
        const value = $(`#${id}`).val();
        if (value) formData.append(id, value);
    });
    generatePdf('/releveprix/pdf-filtre-article-concurrent/', 'rapport_articles_concurrent.pdf', formData.toString());
}

// Fonction pour générer le PDF récapitulatif
function generatePdfRecapitulatif() {
    const selecteur = ['date_debut', 'date_fin'];
    const params = new URLSearchParams();
    selecteur.forEach(id => {
        const value = document.getElementById(id).value;
        if (value) params.append(id, value);
    });
    generatePdf('/releveprix/pdf-recap/', 'rapport_recapitulatif.pdf', params.toString());
}

// Fonction pour générer le PDF Enseigne
function generatePdfEnseigne() {
    generatePdf('/releveprix/pdf-enseigne/', 'rapport_enseigne.pdf', '');
}

// Fonction pour générer le PDF Zone
function generatePdfZone() {
    generatePdf('/releveprix/pdf-zone/', 'rapport_zone.pdf', '');
}

// Fonction pour générer le PDF avec filtres sur les relevés
function generatePdfFilterReleve() {
    const selecteur = ['date-debut', 'date-fin'];
    const params = new URLSearchParams();
    selecteur.forEach(id => {
        const value = document.getElementById(id).value;
        if (value) params.append(id, value);
    });
    generatePdf('/releveprix/pdf-filtre-releve/', 'rapport_releve.pdf', params.toString());
}

// Fonction pour générer le PDF Zone
function generatePdfReleveModal() {
    generatePdf('/releveprix/pdf-releve-modal/', 'rapport_releve_modal.pdf', '');
}

// Fonction pour générer le PDF avec filtres sur les relevés
function generatePdfArticleExterneRattache() {
    const params = new URLSearchParams({
        ref: sessionStorage.getItem("reference"),
    }).toString();
    generatePdf('/releveprix/pdf-article-rattache/', 'rapport_rattachement_article.pdf', params.toString());
}
