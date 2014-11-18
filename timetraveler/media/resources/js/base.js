function click_know_nf(nf_id){
	$.ajax({
		url: "/user/seennewfo",
		type: "POST",
		data: {"nf_id": nf_id},
		success: function(d, s, j){
			var json = $.parseJSON(d);
			if(json.result == "success"){
				$("#newfo-list-"+nf_id).css("display", "none");
				var nf_num = parseInt($("#newf-count").html());
				$("#newf-count").html(nf_num-1);
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

function checkTimeCapsule(){
	$.ajax({
		url: "/timecapsule/check",
		type: "POST",
		data: {},
		success: function(d, s, f){
			var json = $.parseJSON(d);
			if(json.result == "success"){
				var count = json.notis;
				if(count > 0){
					$('#timecapsule-noti-modal').modal('show');
					var str = '你收到了' + count + '个时间囊';
					$('#timecapsule-notifications').html(str);
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

$(document).ready(function(){
	setInterval("checkTimeCapsule()", 5000);
})
