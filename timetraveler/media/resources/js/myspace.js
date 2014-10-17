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
			var json = $.parseJSON(d);
			if (json.result == "success") {
				var comment = json.comment;
				var portrait = json.portrait;
				var user_id = json.user_id;
				var username = json.username;
				var date = json.date;

				var cs = $("#comment-list-"+event_id).html().trim();
				var str = '';
				if (cs != '') str = '<hr>';
				str += '<div class="row"><div class="col-md-1"><img src="/media/' + portrait + '" alt="..." class="img-rounded" height="40" width="40"/></div><div class="col-md-11"><a href="/event/homepage?user_id=' + user_id +'" style="padding-left:10px">' + username + '</a><span style="padding-left:10px" class="pull-right">' + date + '</span><p style="padding-left: 10px">' + comment + '</p></div></div>';
				cs += str;
				$("#comment-list-"+event_id).html(cs);
				$("#comment-list-"+event_id).css("display", "block");
				$("#comment-"+event_id).val('')
			}
			else{
				alert("服务器错误");
			}
		},
		error: function(j, s, e) {
			console.log(e);
		}
	});
}

var status = "";

function set_relation_btn(user_id){
	$.ajax({
		url: "/user/getrelation",
		type: "POST",
		data: {"user_id": user_id},
		success: function(d, s, j){
			var json = $.parseJSON(d);
			if(json.result == "success"){
				if(json.relation == "myself"){
					status = "change_password";
					$("#btn_relation").text("更改密码");
					$("#btn_relation").addClass("btn-primary");
				}
				else if(json.relation == "friend" || json.relation == "hero"){
					status = "following";
					$("#btn_relation").text("正在关注");
					$("#btn_relation").removeClass("btn-danger");
					$("#btn_relation").addClass("btn-success");					
				}	
				else{
					status="dofollow";
					$("#btn_relation").text("+关注");
					$("#btn_relation").addClass("btn-info");
				}

				$("#btn_relation").mouseover(
					function(){
						if(status == "following"){
						status = "unfollow";
						$("#btn_relation").text("取消关注");
						$("#btn_relation").removeClass("btn-success");
						$("#btn_relation").addClass("btn-danger");
						}
					}
				);
				$("#btn_relation").mouseout(
					function(){
						if(status == "unfollow"){
						status = "following";
						$("#btn_relation").text("正在关注");
						$("#btn_relation").removeClass("btn-danger");
						$("#btn_relation").addClass("btn-success");
						}
					}
				);
			}
			else{
				alert("服务器错误");
			}
		},
		error: function(j, s, e){
			console.log(e);
		}
	});
}

function click_relation_btn(user_id){

	var text = $("#btn_relation").text();
	if(status == "change_password"){
		$("#change-password").modal("show");
	}
	else if(status == "unfollow"){
		$.ajax({
			url: "/user/unfollow",
			type: "POST",
			data: {"hero_id": user_id},
			success: function(d, s, j){
				var json = $.parseJSON(d);
				if(json.result == "success"){
					status = "dofollow";
					$("#btn_relation").text("+关注");
					$("#btn_relation").removeClass("btn-danger");
					$("#btn_relation").addClass("btn-info");
					var fan_len = parseInt($("#fan_len").html());
					$("#fan_len").html(fan_len - 1);
				}
				else{
					alert("服务器错误");
				}
			},
			error: function(j, s, e){
				console.log(e);
			}
		});
	}
	else{
		$.ajax({
			url: "/user/follow",
			type: "POST",
			data: {"hero_id": user_id},
			success: function(d, s, j){
				var json = $.parseJSON(d);
				if(json.result == "success"){
					status = "unfollow";
					$("#btn_relation").text("取消关注");
					$("#btn_relation").removeClass("btn-info");
					$("#btn_relation").addClass("btn-danger");
					var fan_len = parseInt($("#fan_len").html());
					$("#fan_len").html(fan_len + 1);
				}
				else{
					alert("服务器错误");
				}
			},
			error: function(j, s, e){
				console.log(e);
			}
		});
	}
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













