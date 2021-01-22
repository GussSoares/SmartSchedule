// all modals reload
$("#ajax.modal").on('hidden.bs.modal', function () {
    $(this).find('.modal-content')
        .html("<div class=\"modal-body\">\n" +
            "          <i class=\"fas fa-sync fa-spin loading-img\"></i>\n" +
            "          <span> &nbsp;&nbsp;Carregando…</span>\n" +
            "        </div>")
});

// all datepickers
$('.date').datepicker({
    daysOfWeekHighlighted: '06',
    format: 'dd/mm/yyyy',
    todayHighlight: true,
    autoclose: true
});

// all select2
$('.select2').select2({
    placeholder: 'Selecione uma opção',
    allowClear: true
})



$("#ajax.modal").on('shown.bs.modal', function () {
    let modal = $('#ajax.modal');
    let modal_cep = modal.find('#id_cep');
    let modal_logradouto = modal.find('#id_logradouro');
    let modal_numero = modal.find('#id_numero');
    let modal_bairro = modal.find('#id_bairro');
    let modal_cidade = modal.find('#id_cidade');
    let modal_uf = modal.find('#id_uf');
    modal_cep.blur(function () {
        if ($(this).val() !== "") {
            $.ajax({
                url: `https://viacep.com.br/ws/${$(this).val()}/json/`,
            }).then(function (data) {
                modal_logradouto.val(data.logradouro)
                modal_numero.val(data.complemento)
                modal_bairro.val(data.bairro)
                modal_cidade.val(data.localidade)
                modal_uf.val(data.uf)
            })
        }
    })
});



// function to create element by html string passed
function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild;
}

// Toast Default
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});


var InitializeMask = (function () {

    var masks = function () {
        $('#id_data_nascimento').inputmask('99/99/9999', { 'placeholder': 'dd/mm/yyyy' })
        $('#id_cpf_cnpj').inputmask('999.999.999-99')
        $('#id_cep').inputmask('99999-999')

        // autocomplete CEP
        $('#id_cep').blur(function () {
            if ($(this).val() !== "") {
                $.ajax({
                    url: `https://viacep.com.br/ws/${$(this).val()}/json/`,
                }).then(function (data) {
                    $('#id_logradouro').val(data.logradouro)
                    // $('#id_numero').val(data.complemento)
                    $('#id_bairro').val(data.bairro)
                    $('#id_cidade').val(data.localidade)
                    $('#id_uf').val(data.uf)
                })
            }
        })
    }

    var maskOnModal = function () {
        $("#ajax.modal").on('shown.bs.modal', function () {
          masks();
        })
    }

    return {
        init: masks,
        initOnModal: maskOnModal
    };
})();

InitializeMask.init();
InitializeMask.initOnModal();
