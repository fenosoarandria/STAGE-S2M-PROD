$('#formPersonnel').on('submit', function(event) {
    event.preventDefault(); 
    // var formData = $(this).serialize(); 
    var formData = new FormData(this);
    $.ajax({
        type: 'POST',
        dataType: 'JSON',
        url: '/addpersonnel/',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            document.getElementById("formPersonnel").reset();
            document.getElementById('profilPers').src = "http://localhost:9090/s2mweb/assets/img/avatar_pers.png";
            swal({
                title: 'Enregistrement effectué avec succès !',
                text: "",
                type: 'success',
                padding: '2em'
              }).then((result) => {
                if (result.isConfirmed) {
                    alert('ok')
                    window.location.href = "{% url '/detailPersonnel/nouveaupers/' %}";
                }
            });
        },
        error: function() {
            
        }
    });
});


$('#updateformPersonnel').on('submit', function(event) {
    event.preventDefault(); 
    // var formData = $(this).serialize(); 
    var formData = new FormData(this);
    $.ajax({
        type: 'POST',
        dataType: 'JSON',
        url: '/updatepersonnel/',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            document.getElementById("formPersonnel").reset();
            document.getElementById('profilPers').src = "http://localhost:9090/s2mweb/assets/img/avatar_pers.png";
            swal({
                title: 'Enregistrement effectué avec succès !',
                text: "",
                type: 'success',
                padding: '2em'
              }).then((result) => {
                if (result.isConfirmed) {
                    alert('ok')
                    window.location.href = "{% url '/detailPersonnel/nouveaupers/' %}";
                }
            });
        },
        error: function() {
            
        }
    });
});

function getservice(val){
    var id = $('#service').val();
    $.ajax({
        type: 'POST',
        dataType: 'JSON',
        url: '/getListDepartement/',
        data: {id:id},
        beforeSend : function () {
            $('#divdepartement').html('');
			},
        success: function(response) {
            console.log(response.html);
            $('#divdepartement').html(response.html); 
        },
        error: function() { 
        }
    });
}

$('#direction').change(function(){
    event.preventDefault(); 
    var id = $('#direction').val();
   
    $.ajax({
        type: 'POST',
        dataType: 'JSON',
        url: '/getListService/',
        data: {id:id},
        beforeSend : function () {
            $('#divservice').html('');
			},
        success: function(response) {
            console.log(response.html);
            $('#divservice').html(response.html); 
        },
        error: function() { 
        }
    });
});

$('#addchild').click(function(){
    event.preventDefault();
    var nb = $('#nbrEnfant').val();
    var nvnb = parseInt(nb, 10) + 1;
    var html = '';
    html += '<div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">';
    html += '<div class="form-group">';
    html += '<label for="" style="font-size: 0.8em;;">ENFANT : </label>';
    html += '<input class="form-control" id="enfant-'+ nvnb +'" name="enfant-'+ nvnb +'" placeholder="NOM ET PRENOM(S)" type="text">';
    html += '</div>';
    html += '</div>';

    html += '<div class="col-xs-4 col-sm-4 col-md-4 col-lg-4"> <div class="form-group">  <label for="" style="font-size: 0.8em;;">DATE DE NAISSAINCE ENFANT: </label>  <input class="form-control" id="datenaiss_enf-'+ nvnb +'" name="datenaiss_enf-'+ nvnb +'" placeholder="" type="date"></div></div>';
    html += '<div class="col-xs-4 col-sm-4 col-md-4 col-lg-4"> <div class="form-group"> <label for="" style="font-size: 0.8em;;">SEXE : </label> <input class="form-control" id="sexe_enf-'+ nvnb +'" name="sexe_enf-'+ nvnb +'" placeholder="" type="text"></div></div>';
    $('#enf').append(html);
    $('#nbrEnfant').val(nvnb);
});


document.getElementById('uploadsary').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profilPers').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});

$('#lead_dir').change(function() {
    if ($(this).prop('checked')) {
        $(this).val('1');  // Si coché, la valeur est '1'
    } else {
        $(this).val('0');  // Sinon, la valeur est '0'
    }
});


