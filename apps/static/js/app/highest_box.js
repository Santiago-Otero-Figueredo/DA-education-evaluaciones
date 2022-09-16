
$(document).ready(function(){
    var highestBox = 0;
    $('.descripcion_etapa', this).each(function(){
        if($(this).height() > highestBox) {
            highestBox = $(this).height();
        }
    });
    $('.descripcion_etapa',this).height(highestBox);
});