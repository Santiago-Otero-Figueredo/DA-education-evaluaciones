if (tipo_etapa == "EtapaAutorizacionPublicacion") {
  var valor = $("#id_autorizo").is(":checked");
  if (valor == false) {
    $("#id_tipo_autorizacion").css("display", "none");
    form_group = $("#id_tipo_autorizacion").parent()
    form_group.css("display", "none");
  }

  $("#id_autorizo").change(function () {
    var autoriza = $("#id_autorizo").is(":checked");
    console.log(autoriza)
    if (autoriza == true) {
      $("#id_tipo_autorizacion").css("display", 'block');
      form_group = $("#id_tipo_autorizacion").parent()
      form_group.css("display", "block");
    }
    else{
        $("#id_tipo_autorizacion").css("display", "none");
        form_group = $("#id_tipo_autorizacion").parent()
        form_group.css("display", "none");
    }
  });

}
