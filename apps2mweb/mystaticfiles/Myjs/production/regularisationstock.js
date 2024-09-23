var tableregularisationproduit = $('#tableregularisationproduit').on('preXhr.dt', function ( e, settings, data ) {
    $('#tabdetail').block({ 
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
        { extend: 'copy', className: 'btn btn-warning btn-rounded btn-sm mb-4' },
        { extend: 'csv', className: 'btn btn-info btn-rounded btn-sm mb-4' },
        { extend: 'excel', className: 'btn btn-success btn-rounded btn-sm mb-4' },
        { extend: 'print', className: 'btn btn-danger btn-rounded btn-sm mb-4' },
        // {
        //     className: 'btn btn-primary btn-rounded btn-sm mb-4' ,
        //     text: 'Retour',
        //     action: function () {
        //         $("#tabindex").show('slow');
        //         $("#tabdetail").hide('slow');
        //         $("#tabbalisage").hide('slow');
        //     },
        // },
    ]
},
"preDrawCallback": function (settings) {
    $('#tabdetail').unblock();
},
"language": {
    "paginate": {
      "previous": "<i class='flaticon-arrow-left-1'></i>",
      "next": "<i class='flaticon-arrow-right'></i>"
    },
    "info": "Showing page _PAGE_ of _PAGES_"
},
"lengthChange": false,
"columnDefs": [
    { width: '50px', targets: 0 },
    { width: '90px', targets: 1 },
    { width: '1000px', targets: 2 },
    { width: '200px', targets: 3 },
    { width: '30px', targets: 4 },
    { width: '30px', targets: 5 },
    { width: '30px', targets: 6 },
    { width: '30px', targets: 7 },
    { width: '30px', targets: 8 },
    {targets: [9,10],className: 'text-right'},
    {targets: [4,5,6,7,8,11,12],className: 'text-center'}
    
],
// "ajax" : {
//     url : '/gestionspromo/Production/',
//     type : 'POST',
//     data : function (request) {
//         request.code = code
//     }
// }   
});