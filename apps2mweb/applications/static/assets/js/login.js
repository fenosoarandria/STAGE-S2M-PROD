$("#seConnecter").on('click', function() {
    var user = $("#utilisateur").val();
    var pswd = $("#mdp").val();
    
    $.ajax({
        url: '/check_login/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ utilisateur: user, mdp: pswd }),
        success: function(response) {
            if (response.success) {
                // // Redirigez vers une autre page pour vérifier le cookie
                window.location.href = window.location.origin + '/accueil/';
            } else {
                showAlert(response.message, 'danger');
                console.error(response.message);  // Affichez un message d'erreur dans la console
                // Affichez une alerte ou un message à l'utilisateur pour des identifiants incorrects
            }
        },
        error: function(xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText);  // En cas d'erreur AJAX
        }
    });
});

