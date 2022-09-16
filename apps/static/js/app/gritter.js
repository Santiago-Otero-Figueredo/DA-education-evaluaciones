function generar_notificacion(tag, mensaje){
    MENSAJES = {
        "success": "Ejecutado correctamente",
        "error": "Error",
        "info": "Información",
        "warning": "Tener en cuenta",
    }
    IMAGENES = {
        "success": "ok.png",
        "error": "error.png",
        "info": "info.png",
        "warning": "alerta.png",
    }
    $.gritter.add({
        title: MENSAJES[tag],
        text: mensaje,
        class_name: 'gritter-'+tag,
        sticky: true,
        image: static_url+"img/estados/"+IMAGENES[tag]
    });
}