$(document).ready( function() {

	$('.btn-file :file').change(function() {
		var filename = $(this).val();
		var s = $(this).parent().children('span');
		s.html(filename.split('\\').pop());
	});
});