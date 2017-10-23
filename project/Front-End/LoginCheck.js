function checkLogin(form){
	if(form.name =="InsTALoginForm"){
		// check condition for Ins/TA to login
		if(form.userName.value == "ta"){
			form.action = "welcome.html";
		}else{
			alert("GIVE ME 4.0!!");
		}
	}
	else{
		// check condition for student to login
		if(form.userName.value =="student"){
			form.action = "welcome.html";
		}else{
			alert("YOU SHALL NOT PASS@_@");
		}
	}
}