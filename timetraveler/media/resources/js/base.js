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
