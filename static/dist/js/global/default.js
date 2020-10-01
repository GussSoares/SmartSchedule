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

// autocomplete CEP
$('#id_cep').blur(function () {
    if ($(this).val() !== "") {
        $.ajax({
            url: `https://viacep.com.br/ws/${$(this).val()}/json/`,
        }).then(function (data) {
            $('#id_logradouro').val(data.logradouro)
            $('#id_numero').val(data.complemento)
            $('#id_bairro').val(data.bairro)
            $('#id_cidade').val(data.localidade)
            $('#id_uf').val(data.uf)
        })
    }
})


// function to create element by html string passed
function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild;
}
