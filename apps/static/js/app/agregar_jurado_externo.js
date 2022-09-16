function obtener_campo_vacio(){
    var form_1 = document.getElementById("id_form-0-nombres")
    if(form_1.value.length > 0){
        var form_2 = document.getElementById("id_form-1-nombres")
        if(form_2.value.length > 0){
            return "2"
        }else{
            return "1"
        }
    }else{
        return "0"
    }
}

function agregar_jurado_externo(id, nombre, apellido, correo, numero_contacto) {
    var checkBox = document.getElementById(id);
    if((checkBox.checked == true) && (!(agregados.includes(id)))){
        var id_formset = obtener_campo_vacio()
        var form_nombre = document.getElementById("id_form-"+id_formset+"-nombres");
        var form_apellido = document.getElementById("id_form-"+id_formset+"-apellidos");
        var form_correo = document.getElementById("id_form-"+id_formset+"-correo");
        var form_numero_contacto = document.getElementById("id_form-"+id_formset+"-numero_contacto");
        agregados.push(id)
        form_nombre.value = nombre
        form_apellido.value = apellido
        form_correo.value = correo
        form_numero_contacto.value = numero_contacto
    }
}