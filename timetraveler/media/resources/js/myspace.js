function do_comment(){
	var text = $("#comment").val();
	if(text == ""){
		alert("评论内容不能为空");
		return;
	}
	$.ajax({
		url: "/event/newcomment",
		type: "POST",
		data
	});

}