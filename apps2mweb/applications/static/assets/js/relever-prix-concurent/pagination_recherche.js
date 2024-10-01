function paginateTable(tableId, paginationId, rowsPerPage) {
    const table = document.getElementById(tableId);
    const pagination = document.getElementById(paginationId);

    if (!table || !pagination) {
        return;
    }

    let currentPage = 1;
    let rows = table.querySelectorAll('tbody tr');
    let filteredRows = Array.from(rows);

    function displayPage(page, rowsToDisplay) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rows.forEach(row => row.style.display = 'none'); 
        rowsToDisplay.slice(start, end).forEach(row => row.style.display = '');
    }

    function setupPagination(rowsToDisplay) {
        const totalPages = Math.ceil(rowsToDisplay.length / rowsPerPage);
        const paginationItems = pagination.querySelector('.pagination');
        if (!paginationItems) {
            console.error(`Pagination list inside "${paginationId}" not found.`);
            return;
        }

        // Reset the pagination content
        paginationItems.innerHTML = '';

        // Create "Précédente" button
        const prevPage = document.createElement('li');
        prevPage.classList.add('page-item');
        prevPage.innerHTML = '<a class="page-link" href="#">Précédente</a>';
        paginationItems.appendChild(prevPage);

        prevPage.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                displayPage(currentPage, rowsToDisplay);
                setupPagination(rowsToDisplay);
            }
        });

        // Create page numbers
        function createPageItem(i) {
            const pageItem = document.createElement('li');
            pageItem.classList.add('page-item');
            pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            if (i === currentPage) {
                pageItem.classList.add('active');
            }

            pageItem.addEventListener('click', (e) => {
                e.preventDefault();
                currentPage = i;
                displayPage(currentPage, rowsToDisplay);
                setupPagination(rowsToDisplay); // Refresh pagination to update active state
            });

            return pageItem;
        }

        // Generate page numbers
        const startPage = Math.max(1, currentPage - 1);
        const endPage = Math.min(totalPages, currentPage + 1);

        for (let i = startPage; i <= endPage; i++) {
            paginationItems.appendChild(createPageItem(i));
        }

        // Create "Suivante" button
        const nextPage = document.createElement('li');
        nextPage.classList.add('page-item');
        nextPage.innerHTML = '<a class="page-link" href="#">Suivante</a>';
        paginationItems.appendChild(nextPage);

        nextPage.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage < totalPages) {
                currentPage++;
                displayPage(currentPage, rowsToDisplay);
                setupPagination(rowsToDisplay);
            }
        });
    }

    displayPage(currentPage, filteredRows);
    setupPagination(filteredRows);

    return {
        update: function(newRows) {
            filteredRows = newRows;
            currentPage = 1;
            displayPage(currentPage, filteredRows);
            setupPagination(filteredRows);
        }
    };
}


function setupSearch(searchId, tableId, paginationInstance) {
    const searchInput = document.getElementById(searchId);
    const table = document.getElementById(tableId);
    const noDataMessage = '<td colspan="100">Aucune donnée disponible</td>'; // Ajustez le colspan selon le nombre de colonnes

    if (!searchInput || !table) {
        // console.error(`Search input with ID "${searchId}" or table with ID "${tableId}" not found.`);
        return;
    }

    const tbody = table.querySelector('tbody');

    // Stocker les lignes d'origine
    const originalRows = Array.from(tbody.querySelectorAll('tr'));

    searchInput.addEventListener('keyup', function() {
        const searchTerm = searchInput.value.toLowerCase();
        let rows;

        if (searchTerm) {
            rows = originalRows.filter(row => {
                const cells = row.querySelectorAll('td');
                const text = Array.from(cells).map(cell => cell.textContent.toLowerCase()).join(' ');
                return text.includes(searchTerm);
            });
        } else {
            rows = originalRows;
        }

        // Réinitialiser le corps du tableau
        tbody.innerHTML = '';

        if (rows.length === 0 && searchTerm) {
            // Afficher le message 'Aucune donnée disponible'
            tbody.innerHTML = noDataMessage;
        } else {
            // Ajouter les lignes filtrées ou toutes les lignes d'origine
            rows.forEach(row => {
                tbody.appendChild(row);
            });
        }

        // Mettre à jour la pagination
        paginationInstance.update(rows);
    });
}
