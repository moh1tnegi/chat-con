$(document).ready(function() {
	$('#uname').keyup(function() {
		if ($(this).val().split(' ').length > 1) {
			$(this).css('margin-bottom', '0');
			$('#no-spc').show();
		}
		else {
			$(this).css('margin-bottom', '20px');
			$('#no-spc').hide();
		}
	});

	$('#passwd').keyup(function() {
		var ps_ln = $(this).val().length;
		$(this).css('margin-bottom', '0');
		if (ps_ln < 6) {
			$('#med-pass').hide();
			$('#str-pass').hide();
			$('#weak-pass').show();
		}
		else if (ps_ln > 5 && ps_ln < 11) {
			$('#weak-pass').hide();
			$('#str-pass').hide();
			$('#med-pass').show();
		}
		else {
			$('#weak-pass').hide();
			$('#med-pass').hide();
			$('#str-pass').show();
		}
	});
	// $('#passwd').blur(function() {
	// 	$(this).css('margin-bottom', '20px');
	// 	$('#weak-pass').hide();
	// 	$('#med-pass').hide();
	// 	$('#str-pass').hide();
	// });

	$('#eml').keyup(function() {
		var eml_rgx = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
		$(this).css('margin-bottom', '0');
		if (eml_rgx.test($(this).val())) {
			$('#inv-eml').hide();
			$('#val-eml').show();			
		}
		else {
			$('#val-eml').hide();
			$('#inv-eml').show();
		}
	});
});