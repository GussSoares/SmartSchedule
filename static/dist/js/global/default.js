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

// function to create element by html string passed
function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes
    return div.firstChild;
}
