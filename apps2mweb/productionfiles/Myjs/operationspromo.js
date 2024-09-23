var debut = "";
var fin = "";
var taboperation = $('#tableoperations').on('preXhr.dt', function ( e, settings, data ) {
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
        { width: '600px', targets: 1 },
        { width: '200px', targets: 2 },
        { width: '200px', targets: 3 },
        { width: '300px', targets: 4 }
    ],
    "ajax" : {
        url : '/rech_operations/',
        type : 'POST',
        data : function (request) {
            request.deb = debut
            request.fin = fin
        }
    }   
});

$("#rech_operations").click(function(){
    
    debut = $("#datedebut").val();
    fin = $("#datefin").val();
    taboperation.ajax.reload();
    
});

var code = "";
var tableDetoperations = $('#tableDetoperations').on('preXhr.dt', function ( e, settings, data ) {
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
            {
            className: 'btn btn-primary btn-rounded btn-sm mb-4' ,
            text: 'Retour',
            action: function () {
                $("#tabindex").show('slow');
                $("#tabdetail").hide('slow');
                $("#tabbalisage").hide('slow');
            },
          },
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
    "ajax" : {
        url : '/detail_operations/',
        type : 'POST',
        data : function (request) {
            request.code = code
        }
    }   
});

function getdetail(key,lib) {
    
    $("#opCode").text(key +' - '+lib);
    $("#tabindex").hide('slow');
    $("#tabdetail").show('slow');
    code = key;
    tableDetoperations.ajax.reload();
    
}


var codePromo = "";
var tableBaloperations = $('#tableBaloperations').on('preXhr.dt', function ( e, settings, data ) {
        $('#tabbalisage').block({ 
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
            { extend: 'csv', className: 'btn btn-info btn-rounded btn-sm mb-4' },
            { extend: 'excel', className: 'btn btn-success btn-rounded btn-sm mb-4' },
            {
                className: 'btn btn-warning btn-rounded btn-sm mb-4' ,
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">Imprimer petit format</span>',
                action: function () {
                    
                    getLst_check();
                },
            },
            {
                className: 'btn btn-default btn-rounded btn-sm mb-4' ,
                text: '<span class="glyphicon glyphicon-print" aria-hidden="true">Imprimer grand format</span>',
                action: function () {
                    
                    getLst_checkGF();
                },
            },
            {
                className: 'btn btn-primary btn-rounded btn-sm mb-4' ,
                text: 'Retour',
                action: function () {
                    $("#tabindex").show('slow');
                    $("#tabdetail").hide('slow');
                    $("#tabbalisage").hide('slow');
                },
            },
        ]
    },
    "preDrawCallback": function (settings) {
        $('#tabbalisage').unblock();
    },
    "language": {
        "paginate": {
          "previous": "<i class='flaticon-arrow-left-1'></i>",
          "next": "<i class='flaticon-arrow-right'></i>"
        },
        "info": "Showing page _PAGE_ of _PAGES_"
    },
    "lengthChange": false,
    // "scrollY": "1000px",          
    "pageLength": 15000,
    "columnDefs": [
        { width: '20px', targets: 0 },
        { width: '900px', targets: 1 },
        { width: '200px', targets: 2 },
        { width: '200px', targets: 3 },
        { width: '20px', targets: 4 },
        { width: '50px', targets: 5 },
        {targets: [2,3],className: 'text-right'}
    ],
    "ajax" : {
        url : '/Bal_operations/',
        type : 'POST',
        data : function (request) {
            request.code = codePromo
        }
    }   
});


function balisage(key,lib) {
    
    $("#opbalCode").text(key +' - '+lib);
    $("#tabindex").hide('slow');
    $("#tabdetail").hide('slow');
    $("#tabbalisage").show('slow');
    codePromo = key;
    tableBaloperations.ajax.reload();

};


/****************** debut PDF balisage***********************/

function getLst_checkGF(){

    var newTab = new Array();
    newTab['libelle'] = new Array();
    newTab['pVenteNormale'] = new Array();
    newTab['pVentePromo'] = new Array();
    newTab['nbr'] = new Array();
    newTab['format'] = new Array();
    var tempTab = new Array();
    tempTab['libelles'] = new Array();
    tempTab['pVenteNormales'] = new Array();
    tempTab['pVentePromos'] = new Array();
    tempTab['format'] = new Array();

    var i = 0;

    $('table#tableBaloperations TBODY tr').each(function(){
        
        var libelle = $(this).find('td').eq(1).text();
        var venteNorm = $(this).find('td').eq(2).text();
        var ventePromo = $(this).find('td').eq(3).text();
        var nbrImprim = $(this).find("td:eq(4) input[type='number']").val();
        var format = $(this).find("td:eq(5) option:selected").val();
        if(nbrImprim != "" && format != "0")
        {
            newTab['libelle'][i] = libelle;
            newTab['pVenteNormale'][i] = venteNorm;
            newTab['pVentePromo'][i] = ventePromo;
            newTab['nbr'][i] = nbrImprim;
            newTab['format'][i] = format;
            for(p = 0; p < nbrImprim; p++){
                tempTab['libelles'].push(libelle);
                tempTab['pVenteNormales'].push(venteNorm);
                tempTab['pVentePromos'].push(ventePromo);
                tempTab['format'].push(format);
            }
            
        }
        i++;
    });

    var doc = new jsPDF();
    var x = 30;
    var y = 60;
    var cptr = 0;
    var index = 0;
    for(l = 0; l < tempTab['libelles'].length; l++){
        if(tempTab['format'][l] == "GrandFormat"){
            arti = tempTab['libelles'][l];
            pxNorm = tempTab['pVenteNormales'][l];
            prixProm = tempTab['pVentePromos'][l];
            if(index == 4){
                doc.addPage();
                x = 30;
                y = 43;
                index = 0;
            }
                doc.setFontSize(20);
                doc.text(arti.substr(0,24), 100, y);
                doc.setFontSize(70);
                doc.text(prixProm+' Ar', 100, parseInt(y)+ parseInt(25));
                doc.setFontSize(30);
                doc.setLineWidth(0.5);
                doc.line(150, parseInt(y)+ parseInt(33), 180, parseInt(y)+ parseInt(33));
                doc.text(pxNorm+' Ar', 150, parseInt(y)+ parseInt(35));
                y = y + 100;
            index ++;
        }
    }
    doc.output("dataurlnewwindow");
}

function getLst_check()
{
    var newTab = new Array();
    newTab['libelle'] = new Array();
    newTab['pVenteNormale'] = new Array();
    newTab['pVentePromo'] = new Array();
    newTab['nbr'] = new Array();
    newTab['format'] = new Array();
    var tempTab = new Array();
    tempTab['libelles'] = new Array();
    tempTab['pVenteNormales'] = new Array();
    tempTab['pVentePromos'] = new Array();
    tempTab['format'] = new Array();

    var i = 0;
    $('table#tableBaloperations TBODY tr').each(function(){
        
        var libelle = $(this).find('td').eq(1).text();
        var venteNorm = $(this).find('td').eq(2).text();
        var ventePromo = $(this).find('td').eq(3).text();
        var nbrImprim = $(this).find("td:eq(4) input[type='number']").val();
        var format = $(this).find("td:eq(5) option:selected").val();
        if(nbrImprim != "" && format != "0")
        {
            newTab['libelle'][i] = libelle;
            newTab['pVenteNormale'][i] = venteNorm;
            newTab['pVentePromo'][i] = ventePromo;
            newTab['nbr'][i] = nbrImprim;
            newTab['format'][i] = format;
            for(p = 0; p < nbrImprim; p++){
                tempTab['libelles'].push(libelle);
                tempTab['pVenteNormales'].push(venteNorm);
                tempTab['pVentePromos'].push(ventePromo);
                tempTab['format'].push(format);
            }
        }

        i++;
    });

    var doc = new jsPDF();
    var x = 20;
    var y = 90;
    var cptr = 0;
    var index = 0;

    for(l = 0; l < tempTab['libelles'].length; l++){
        if(tempTab['format'][l] == "PetitFormat"){
            arti = tempTab['libelles'][l];
            pxNorm = tempTab['pVenteNormales'][l];
            prixProm = tempTab['pVentePromos'][l];
            if(index == 4){
                doc.addPage();
                x = 20;
                y = 90;
                index = 0;
            }
            if(index%2 == 1){
                doc.setFontSize(14);
                doc.text(arti.substr(0,24), x, y);
                doc.setFontSize(45);
                doc.text(prixProm+' Ar', 40, parseInt(y)+ parseInt(20));
                doc.setFontSize(20);
                doc.setLineWidth(0.5);
                doc.line(60, parseInt(y)+ parseInt(28), 80, parseInt(y)+ parseInt(28));
                doc.text(pxNorm+' Ar', 60, parseInt(y)+ parseInt(30));
                y = y + 130;
            }else{
                doc.setFontSize(14);
                doc.text(arti.substr(0,24), 130, y);
                doc.setFontSize(45);
                doc.text(prixProm+' Ar', 130, parseInt(y)+ parseInt(20));
                doc.setFontSize(20);
                doc.setLineWidth(0.5);
                doc.line(150, parseInt(y)+ parseInt(28), 170, parseInt(y)+ parseInt(28));
                doc.text(pxNorm+' Ar', 150, parseInt(y)+ parseInt(30));
            }
            index ++;
        }
    }
    doc.output("dataurlnewwindow");
}

/****************** fin PDF balisage***********************/