var transformationtable = $('#transformationtable').on('preXhr.dt', function ( e, settings, data ) {
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
    { width: '200px', targets: 4 },
    { width: '200px', targets: 5 }
],  
// ajax: {
//     url: '/gestionspromo/production/',  // L'URL de votre endpoint Django pour récupérer les données de production
//     type: 'POST',
//     data: function (request) {
//         console.log(request)
//     }
// }
});
