
    $(window).scroll(function() {
	    if($(this).scrollTop() > 500) {
	        $('.navbar').addClass('opaq-nav');
	    }
	    else {
	        $('.navbar').removeClass('opaq-nav');
	    }
	});