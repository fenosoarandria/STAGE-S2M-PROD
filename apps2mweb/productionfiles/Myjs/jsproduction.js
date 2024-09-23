var debut = "";
var fin = "";
var taboperation = $('#tableproductions').on('preXhr.dt', function ( e, settings, data ) {
        $('#tableproductions').block({ 
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
            { extend: 'copy', className: 'btn btn-warning btn-rounded btn-sm mt-4' },
            { extend: 'csv', className: 'btn btn-info btn-rounded btn-sm' },
            { extend: 'excel', className: 'btn btn-success btn-rounded btn-sm' },
            { extend: 'print', className: 'btn btn-danger btn-rounded btn-sm' }
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
        $('#tableproductions').unblock();
    },
    "lengthChange": false,
    "columnDefs": [
        { width: '100px', targets: 0 },
        { width: '300px', targets: 1 },
        { width: '500px', targets: 2 },
        { width: '300px', targets: 3 },
        { width: '200px', targets: 4 }
    ] 
});
