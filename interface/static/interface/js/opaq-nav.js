$(document).ready(function() {
	$(window).scroll(function() {
	    if($(this).scrollTop() > 600) {
	        $('.navbar').addClass('opaq-nav');
	    }
	    else {
	        $('.navbar').removeClass('opaq-nav');
	    }
	});
});