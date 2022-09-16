
function startIntro() {
    
    var intro = introJs();
    intro.setOptions({
        steps: lista_elementos_menu,
        showProgress: true
    });
    intro.setOptions({ 'nextLabel': 'Siguiente', 'prevLabel': 'Atrás', 'doneLabel': 'Hecho' });

    intro.onbeforechange(function(element) {
        $.gritter.removeAll();
        if (element.className == 'dropdown-item') {
            $("#page-container").removeClass("has-scroll");
            $("#expandir_opciones").attr("aria-expanded","true");
            $("#menu_opciones_usuario").addClass('show');
            $("#sub_menu_opciones").addClass('show');
            $("#sub_menu_opciones").css("position", "absolute");
            $("#sub_menu_opciones").css("inset", "0px 0px auto auto");
            $("#sub_menu_opciones").css("margin", "0px");
            $("#sub_menu_opciones").css("transform", "translate(0px, 52px)");
            $("#sub_menu_opciones").attr("data-popper-placement","bottom-end");
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });

    intro.onexit(function(element) {
        $("#expandir_opciones").attr("aria-expanded","false")
        $("#menu_opciones_usuario").removeClass('show');
        $("#sub_menu_opciones").removeClass('show');

    });

    intro.start();
}
