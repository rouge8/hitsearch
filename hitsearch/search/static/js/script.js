$(document).ready(function() {
    $('#toggleTweakBox').click(function() {
        if ($('#tweakBox').is(':visible')) {
            $('#tweakBox').slideUp('fast');
            createCookie("showTweakBox", 0);
        }
        else {
            $('#tweakBox').slideDown('fast');
            createCookie("showTweakBox", 1);
        }
    });
    
    $('#betaSlider').slider({
    	range: "min",
        value: parseFloat($('#b').val()) * 100,
        min: 0,
        max: 100,
        slide: function( event, ui ) {
		    $('#betaSliderValue').text((ui.value / 100).toFixed(2));
		    $('#b').val(ui.value / 100);
		}
    });
    
    $('#sortByRadio').buttonset();
    
    var showTweakBox = readCookie("showTweakBox");
    if (showTweakBox == 1) { $('#tweakBox').show(); }
    
});