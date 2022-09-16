var handleScheduleCalendar = function() {
	$("#schedule-calendar").simpleCalendar({
		months: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        days: ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'],
		fixedStartDay: true,
		disableEmptyDetails: true,
		events: fechas_limites
	});
};

var dashboard = function () {
	"use strict";
	return {
		//main function
		init: function () {
			handleScheduleCalendar();
		}
	};
}();

$(document).ready(function() {
	dashboard.init();
});