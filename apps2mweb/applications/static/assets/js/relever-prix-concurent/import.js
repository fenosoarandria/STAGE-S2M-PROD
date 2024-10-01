document.addEventListener("DOMContentLoaded", function() {
    function handleSectionToggle(showSectionId, hideSectionId, activeLinkId, inactiveLinkId) {
        const showSection = document.getElementById(showSectionId);
        const hideSection = document.getElementById(hideSectionId);
        const activeLink = document.getElementById(activeLinkId);
        const inactiveLink = document.getElementById(inactiveLinkId);

        if (showSection) showSection.style.display = "block";
        if (hideSection) hideSection.style.display = "none";
        
        if (activeLink) activeLink.classList.add("active");
        if (inactiveLink) inactiveLink.classList.remove("active");
    }

    // Vérifier l'existence des éléments avant d'ajouter des événements
    const nommLink = document.getElementById("nomm");
    const impoExcLink = document.getElementById("impoExc");

    if (nommLink) {
        nommLink.addEventListener("click", function(event) {
            event.preventDefault();
            handleSectionToggle("nomenclature-section", "import-excel-releve", "nomm", "impoExc");
        });
    }

    if (impoExcLink) {
        impoExcLink.addEventListener("click", function(event) {
            event.preventDefault();
            handleSectionToggle("import-excel-releve", "nomenclature-section", "impoExc", "nomm");
        });
    }

    // Afficher par défaut la section "NOMENCLATURES" et styliser le lien correspondant
    handleSectionToggle("nomenclature-section", "import-excel-releve", "nomm", "impoExc");
});

async function uploadFileReleve() {
    const zoneMap = {
        'TANANARIVE': 712, 'TANA': 712, 'ANTANANARIVO': 712,
        'TAMATAVE': 713, 'TAMATAVY': 713,
        'MAHAJUNGA': 715, 'MAHAJANGA': 715,
        'DIEGO': 717, 'ANTSIRANANA': 717,
        'TULEAR': 719, 'TOLIARA': 719,
        'FIANARANTSOA': 726
    };

    const zone = document.getElementById('id_zone').value;
    const enseigne = document.getElementById('id_enseigne').value;
    const num_releve = sessionStorage.getItem('num_releve');
    const mag = zoneMap[zone] || 712;
    const file = document.getElementById('importExcelReleve').files[0];
    console.log(num_releve)
    console.log(enseigne)
    if (!file) {
        alert('Veuillez sélectionner un fichier.');
        return;
    }

    const formData = new FormData();
    formData.append('importExcel', file);
    formData.append('num_releve', num_releve);
    formData.append('zone', zone);
    formData.append('enseigne', enseigne);
    formData.append('mag', mag);

    try {
        const response = await fetch("/releveprix/import-releve/", {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
        });

        const data = await response.json();
        showAlert(data.data, 'success');
        $('#nouveauArticleModal').modal('hide');
        DetailReleve(num_releve);
        applyFiltersReleveIndex();

    } catch (error) {
        showAlert(data.data, 'danger');
        console.error('Erreur lors de l\'importation:', error);
    }
}

async function uploadFileRattachementS2M() {
    const file = document.getElementById('importExcelRattachementS2M').files[0];
    console.log(file)
    if (!file) {
        showAlert('Veuillez sélectionner un fichier.', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('importExcelRattachement', file);
    showLoading();
    try {
        const response = await fetch("/releveprix/import-rattachement-article-exel/", {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
        });
        const data = await response.json();
        if (data.success) {   
            $('#rattachementModal').modal('hide');
            hideLoading();
            showAlert(data.message, 'success');
        }else{
            showAlert(data.message, 'danger');
        }
    } catch (error) {
        showAlert(data.data, 'danger');
        hideLoading();
        console.error('Erreur lors de l\'importation:', error);
    }
}

async function uploadFileRattachementConcurrent() {
    const file = document.getElementById('importExcelRattachementConcurrent').files[0];

    if (!file) {
        showAlert('Veuillez sélectionner un fichier.', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('importExcelRattachementConcurrent', file);
    showLoading();
    try {
        const response = await fetch("/releveprix/import-rattachement-concurrent-exel/", {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
        });
        const data = await response.json();
        if (data.success) {
            $('#rattachementConcurrentModal').modal('hide');
            hideLoading();
            showAlert(data.message, 'success');
        }else{
            showAlert(data.message, 'danger');
        }
    } catch (error) {
        showAlert(data.message, 'danger');
        hideLoading();
        console.error('Erreur lors de l\'importation:', error);
    }
}


async function uploadFileReleveConcurrent() {
    const zone = document.getElementById('id_zone').value;
    const enseigne = document.getElementById('id_enseigne').value;
    const num_releve = sessionStorage.getItem('num_releve');
    
    const file = document.getElementById('importExcelRattachement').files[0];

    if (!file) {
        alert('Veuillez sélectionner un fichier.');
        return;
    }

    const formData = new FormData();
    formData.append('importExcel', file);
    formData.append('num_releve', num_releve);
    formData.append('zone', zone);
    formData.append('enseigne',enseigne );

    try {
        const response = await fetch("/releveprix/import-releve-concurrent/", {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
        });

        const data = await response.json();
        if (data.success) {
            showAlert(data.message, 'success');
            $('#nouveauArticleConcurrentModal').modal('hide');
            DetailReleve(num_releve);
            applyFiltersReleveIndex();
        }else{
            showAlert(data.message, 'danger');
        }

    } catch (error) {
        showAlert(data.message, 'danger');
        console.error('Erreur lors de l\'importation:', error);
    }
}
