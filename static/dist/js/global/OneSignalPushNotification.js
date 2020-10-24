window.OneSignal = window.OneSignal || [];
OneSignal.push(function() {


    function save_player_id () {
        OneSignal.getUserId().then(function(userId) {
            console.log("OneSignal User ID:", userId);
            if (userId) {
                $.ajax({
                    url: url_register_player_id,
                    method: 'post',
                    async: false,
                    data: {
                        csrfmiddlewaretoken: csrf_token,
                        player_id: userId,
                        member_id: member_id
                    }
                })
            }
        });
    }

    OneSignal.getUserId().then(function (userId) {
        /*
        * Verifica se o playerid recebido é diferente do cadastrado para o usuário.
        * Se o playerid salvo nao bater com o recebido, pergunta se quer receber notificacao
        * e salva o playerid
        */
        if (member_player_id != userId || membe_player_id == '' || userId == null) {
            /*
            * Sempre que esta página for acessada, após 1 segundo, apresentará um modal
            * que avisará sobre as notificações. Ao permitir, serão enviadas notificações
            * para o ultimo dispositivo cuja autorização foi dada.
            */
            setTimeout(function () {
                Swal.fire({
                    icon: 'question',
                    title: 'Olá! 📅 Quer receber lembrete da escala?',
                    text: 'Basta clicar em "permitir" no popup que irá aparecer. 😎',
                    showCloseButton: false,
                    showCancelButton: false,
                    onClose: function () {
                        OneSignal.init({
                            appId: ONESIGNAL_APP_ID,
                            autoRegister: true
                        });
                        OneSignal.registerForPushNotifications({
                            appId: ONESIGNAL_APP_ID,
                            modalPrompt: false
                        });

                        save_player_id();
                    }
                })
            }, 1000)
        }
    });
});
