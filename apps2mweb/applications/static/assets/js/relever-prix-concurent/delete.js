function setupDeleteReleve() {
    $(document).ready(function() {
        let itemId;
        // Lorsque le bouton de suppression est cliqué, stocker l'ID dans une variable
        $('.btn-delete').off('click').on('click', function() {
            itemId = $(this).data('id');
        });
        
        // Lorsque le bouton de confirmation de suppression est cliqué, envoyer la requête de suppression
        $('#deleteReleveForm .btn-danger').off('click').on('click', function() {
            if (!itemId) {
                console.error('Aucun ID spécifié pour la suppression.');
                return;
            }
            
            fetch(`/releveprix/delete-releve/`, {
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
                if (data.success) {
                    $(`button[data-id="${itemId}"]`).closest('tr').remove();
                    Releve();
                    applyFiltersReleveIndex();
                    const paginationReleve = paginateTable('table-releve', 'pagination-releve', 5);
                    setupSearch('searchReleveInput', 'table-releve', paginationReleve);
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.message, 'danger');
                }
                $('#deleteReleveModal').modal('hide');
            })
            .catch(error => {
                console.error('Erreur:', error);
                showAlert('Une erreur est survenue.', 'danger');
                $('#deleteReleveModal').modal('hide');
            });
        });
    });
}
