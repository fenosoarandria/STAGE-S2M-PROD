
var base_url = '{{ base_url }}';
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Récupérez le jeton CSRF du cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$('#telechargerCertificat').on('click', function (sidebar) {
	var db = $('#date_debut').val();
	var fn = $('#date_fin').val(); 
    var matricule = $('#matricule').val();
	$.ajax({
        url: 'certificatTravail/',
        type: 'POST',
        dataType: 'JSON',
        data: {db : db, fn : fn, matricule:matricule},
        beforeSend: function(xhr, settings) {
        	/*xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));*/
    	},
        success : function (result) {
            window.open(result.nom, "_blank");
            $('#modalcertificat').modal('hide');
        }
    });
})

$('#telechargerAttestation').on('click', function (sidebar) {
    var db = $('#date_debutct').val();
    var contrat = $('#contrat').val(); 
    var matricule = $('#matriculect').val();
    alert('ok');
    $.ajax({
        url: 'attestationTravail/',
        type: 'POST',
        dataType: 'JSON',
        data: {db : db, contrat : contrat, matricule:matricule},
        beforeSend: function(xhr, settings) {
            /*xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));*/
        },
        success : function (result) {
            window.open(result.nom, "_blank");
            $('#modalattestation').modal('hide');
        }
    });
})
