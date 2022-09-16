$('#id_borrador').on('change', function() {
    asunto = $( "#id_borrador option:selected").text()

    $(borradores).each(function(indice, valor){
        if (asunto === valor['asunto']){
            $("#id_asunto").val(asunto);
            $("#id_mensaje").val(valor['descripcion']);
        }

    });
});

$("#limpiar").click(function(e){
    console.log("buenas");
    e.preventDefault();
    $("#id_asunto").val("");
    $("#id_mensaje").val("");
    $( "#id_borrador").val(0)
}); 