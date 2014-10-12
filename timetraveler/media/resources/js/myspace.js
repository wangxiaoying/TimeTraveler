function do_comment(event_id){
	var text = $("#comment-"+event_id).val();
	if(text == ""){
		alert("评论内容不能为空");
		return;
	}
	
	$.ajax({
		url: "/event/newcomment",
		type: "POST",
		data: {"text": text, "event_id": event_id},
		success: function(d, s, j) {
			var json = $.parseJSON(d)
			if (json.result == "success") {
				var comment = json.comment;
				var portrait = json.portrait;
				var username = json.username
				var date = json.date

				var cs = $("#comment-list-"+event_id).html().trim();
				var str = '';
				if (cs != '') str = '<hr>';
				str += '<div class="row"><div class="col-md-1"><img src="/media/' + portrait + '" alt="..." class="img-rounded" height="40" width="40"/></div><div class="col-md-11"><a href="#" style="padding-left:10px">' + username + '</a><span style="padding-left:10px" class="pull-right">' + date + '</span><p style="padding-left: 10px">' + comment + '</p></div></div>';

				cs += str;
				$("#comment-list-"+event_id).html(cs);
				$("#comment-list-"+event_id).css("display", "block");
				$("#comment-"+event_id).val('')
			}
			else{
				alert("服务器错误")
			}
		},
		error: function(j, s, e) {
			console.log(e);
		}
	});
}

$(document).ready( function() {

	$('.btn-file :file').change(function() {
		var filename = $(this).val();
		var s = $(this).parent().children('span');
		s.html(filename.split('\\').pop());
	});

	$('.comment-input').on('keyup', function(event) {
		if (event.which == 13) {
			var event_id = $(this).context.id.split('-').pop();
			do_comment(event_id);
		}
	})
});













