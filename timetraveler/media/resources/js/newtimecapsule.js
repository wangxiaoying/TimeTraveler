$(document).ready(function (){
	$('.btn-file :file').change(function() {
		console.log('hahaha');
		var filename = $(this).val();
		var s = $(this).parent().children('span');
		s.html(filename.split('\\').pop());
		console.log(filename);
	});
});

function searchFriends(){
	
}