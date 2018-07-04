$(document).ready(function() {
	if($(this).scrollTop() > 0) {
		$('.navbar').addClass('opaq-nav');
		$('#down-button').hide();
	}
	else {
		$('#down-button').show();		
	}

	$(window).scroll(function() {
		if($(this).scrollTop() > 100) {
	    	$('#down-button').fadeOut();
		}
		else {
	    	$('#down-button').fadeIn();
		}
		if($(this).scrollTop() > 500) {
			$('.navbar').addClass('opaq-nav');
		}
		else {
			$('.navbar').removeClass('opaq-nav');
		}
		// $('#down-button').click();
	});

	$('#down-button').click(function() {
		$('html, body').animate({scrollTop: 600}, 800);
	    $('.navbar').addClass('opaq-nav');
	    $(this).fadeOut();
	});
});
