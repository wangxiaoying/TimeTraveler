function validate_password(){
	var p1 = $("#registerInputPassword").val();
	var pc = $("#registerInputPasswordConfirm");
	var p2 = pc.val();
	if(p1 != p2){
		pc.popover('show');
		return false;
	}
	return true;
}