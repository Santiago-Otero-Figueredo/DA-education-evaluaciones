function agregar_jurado_interno(id, id_jurado, nombre) {
    var checkBox = document.getElementById(id);
    if((checkBox.checked == true) && (!(agregados.includes(id)))){
        valores_select.push(id_jurado)
        console.log($('#id_internos').val())
        $('#id_internos').val(valores_select).trigger('change')
        agregados.push(id)
    }
}