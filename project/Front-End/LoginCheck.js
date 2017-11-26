function checkLogin(form){
	if(form.name =="InsTALoginForm"){
		// check condition for Ins/TA to login
		if(form.userName.value == "ta" &&
 		   form.password.value == "im ta"){
			form.action = "welcome.html";
		}else{
			alert("GIVE ME 4.0!!");
			form.action = "./InsTaLgin.html";
		}
	}
	else{
		// check condition for student to login
		if(form.userName.value =="student" &&
                   form.password.value == "I<3C01"){
			form.action = "welcome.html";
		}else{
			alert("YOU SHALL NOT PASS@_@");
			form.action = "./studentLgin.html";
		}
	}
}
