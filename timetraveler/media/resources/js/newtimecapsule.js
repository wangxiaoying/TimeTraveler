$(document).ready(function (){
	$('.btn-file :file').change(function() {
		console.log('hahaha');
		var filename = $(this).val();
		var s = $(this).parent().children('span');
		s.html(filename.split('\\').pop());
		console.log(filename);
	});
});

function to_someone(who){
	var keyword = $('#search-rp').val();
	$.ajax({
		url: "/user/getuserlist",
		type: "POST",
		data: {"who": who, "keyword": keyword} ,
		success: function(d, s, j){
			var json = $.parseJSON(d);
			if(json.result == "success"){
				$("#rp-list").modal('show');
				if(0 == json.users.length){
					$("#userlist-body").html('<h3>没有搜到任何用户</h3>');
				}else{
					var str = '<div class="list-group row">';
					for(var i = 0; i < json.users.length; ++i){
						str += '<a class="list-group-item col-md-2" onclick="choose_rp('+ json.users[i].user_id +')">';
						str += '<img src="/media/' + json.users[i].portrait + '" class="img-rounded" height="50" width="50" alt="..."/>';
						str += '<h3>' + json.users[i].username + '</h3>'
						str += '</a>';
					}
					str += '</div>'
					$("#userlist-body").html(str);
				}
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

function choose_rp(id){
	$.ajax({
		url: "/user/getbyid",
		type: "POST",
		data: {"user_id": id} ,
		success: function(d, s, j){
			var json = $.parseJSON(d);
			if(json.result == "success"){
				$('#rp_name').html(json.username);
				var portrait = '/media/' + json.portrait;
				$('#rp_img').attr('src', portrait);
				// $('#user_to_id').attr('value', id);
				$('#user_to_id').val(id);
				console.log($('#user_to_id').val());
			}
			else{
				alert("服务器错误");
			}
			$("#rp-list").modal('hide');
		},
		error: function(j, s, e){
			console.log(e);
		}
	});
}