/** page création production */
var productiontable = $('#productiontable').on('preXhr.dt', function ( e, settings, data ) {
    $('#tabindex').block({ 
        message: '<div class="loader"></div>',
        overlayCSS: {
            backgroundColor: '#fff',
            opacity: 0.8,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'transparent'
        }
    });       
}).DataTable({
    dom: '<"row"<"col-md-12"<"row"<"col-md-6"B><"col-md-6"f> > ><"col-md-12"rt> <"col-md-12"<"row"<"col-md-5 mb-md-0 mb-5"i><"col-md-7"p>>> >',
    buttons: {
        buttons: [
            { extend: 'copy', className: 'btn btn-warning btn-rounded btn-sm mb-4', 
                exportOptions: {
                    columns: [0, 1, 2, 3],
                } 
            },
            { extend: 'csv', className: 'btn btn-info btn-rounded btn-sm mb-4',

                exportOptions: {
                    columns: [0, 1, 2, 3],
                } 

            },
            { extend: 'excel', className: 'btn btn-success btn-rounded btn-sm mb-4',

                exportOptions: {
                    columns: [0, 1, 2, 3],
                } 
            },
            { extend: 'print', className: 'btn btn-danger btn-rounded btn-sm mb-4',

                exportOptions: {
                    columns: [0, 1, 2, 3],
                } 
            }
        ]
    },
    "language": {
        "paginate": {
            "previous": "<i class='flaticon-arrow-left-1'></i>",
            "next": "<i class='flaticon-arrow-right'></i>"
        },
        "info": "Showing page _PAGE_ of _PAGES_"
    },
    "preDrawCallback": function (settings) {
        $('#tabindex').unblock();
    },
    "lengthChange": false,
    "columnDefs": [
        { width: '100px', targets: 0 },
        { width: '400px', targets: 1 },
        { width: '500px', targets: 2 },
        { width: '200px', targets: 3 },
        { width: '200px', targets: 4 }
    ],  
    ajax: {
        url: '/gestionspromo/production/',  // L'URL de votre endpoint Django pour récupérer les données de production
        type: 'POST',
        data: function (request) {
            console.log(request)
        }
    }
});


/** page détail production */
var detailproductionstable = $('#detailproductionstable').on('preXhr.dt', function ( e, settings, data ) {
    $('#tabindex').block({ 
        message: '<div class="loader"></div>',
        overlayCSS: {
            backgroundColor: '#fff',
            opacity: 0.8,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'transparent'
        }
    });       
}).DataTable({
dom: '<"row"<"col-md-12"<"row"<"col-md-6"B><"col-md-6"f> > ><"col-md-12"rt> <"col-md-12"<"row"<"col-md-5 mb-md-0 mb-5"i><"col-md-7"p>>> >',
buttons: {
    buttons: [
        { extend: 'copy', className: 'btn btn-warning btn-rounded btn-sm mb-4', 
            exportOptions: {
              columns: [0, 1, 2, 3],
            } 
        },
        { extend: 'csv', className: 'btn btn-info btn-rounded btn-sm mb-4',

            exportOptions: {
              columns: [0, 1, 2, 3],
            } 

        },
        { extend: 'excel', className: 'btn btn-success btn-rounded btn-sm mb-4',

            exportOptions: {
              columns: [0, 1, 2, 3],
            } 
        },
        { extend: 'print', className: 'btn btn-danger btn-rounded btn-sm mb-4',

            exportOptions: {
              columns: [0, 1, 2, 3],
            } 
        }
    ]
},
"language": {
    "paginate": {
      "previous": "<i class='flaticon-arrow-left-1'></i>",
      "next": "<i class='flaticon-arrow-right'></i>"
    },
    "info": "Showing page _PAGE_ of _PAGES_"
},
"preDrawCallback": function (settings) {
    $('#tabindex').unblock();
},
"lengthChange": false,
"columnDefs": [
    { width: '100px', targets: 0 },
    { width: '400px', targets: 1 },
    { width: '500px', targets: 2 },
    { width: '200px', targets: 3 },
    { width: '200px', targets: 4 }
],  
ajax: {
    url: '/gestionspromo/detail_production/',  // L'URL de votre endpoint Django pour récupérer les données de production
    type: 'POST',
    data: function (request) {
        console.log(request)
    }
}
});


$("#addButton").on('click', function() {
    // console.log('Tena tonga ato tokoa ve.');

    // Obtenir la date et l'heure actuelles
    const now = new Date();
    const offset = now.getTimezoneOffset(); // Décalage en minutes par rapport à UTC
    const localDateTime = new Date(now.getTime() - offset * 60000); // Ajuster en fonction du décalage
    const dateTime = localDateTime.toISOString().replace('T', ' ').split('.')[0]; // Format YYYY-MM-DD HH:MM:SS

    // Données à envoyer au serveur
    const data = {
        date: dateTime,           // Date actuelle
        personnel: '8888',   // Remplacer par la valeur réelle si nécessaire
        details: '5'
    };

    // URL de l'API ou de la vue Django où la fonction insertionProduction est définie
    const url = '/gestionspromo/insertionProduction/';

    // Options de la requête Fetch
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    // Faire la requête Fetch
    fetch(url, options)
    .then(response => response.text())  // Lire la réponse comme texte brut
    .then(text => {
        console.log('Réponse brute du serveur:', text);
        try {
            const result = JSON.parse(text);  // Essayer de parser en JSON
            if (result.success) {
                console.log(result.message);  // Affiche "Insertion réussie!" en cas de succès
                window.location.href = '/gestionspromo/getproduction/';
            } else {
                console.error(result.message);  // Affiche le message d'erreur en cas d'échec
            }
        } catch (e) {
            console.error('Erreur lors de l\'analyse JSON:', e);
        }
    })
    .catch(error => console.error('Erreur lors de la requête Fetch:', error));
});


