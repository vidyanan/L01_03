var filecontent;


/* read the file content into globle variable filecontent
 * @files The list of files uploaded in the file input
 */
function readFile(files) {
      var file = files[0];
      var reader = new FileReader();
      reader.onload = function (e) {
	    filecontent = e.target.result;
      };
      reader.readAsText(file);
    }



function createAccount() {

    // get the email in the form
    var email=document.getElementById("email").value;
    // get the password in the form
    var password=document.getElementById("password").value;
    // extract emails and passwords of students into diferrent variable from filecontent
    var list_of_emails="";
    var list_of_passwords="";
    var is_email = true;
    var i = 0;
    // start at the first charactor in the filecontent
    while (i < filecontent.length){
    	// next substring separated by space is email
    	if(is_email){
    		var endIndex = i + filecontent.substring(i,filecontent.length).indexOf(" ");
    		var next_email = filecontent.substring(i,endIndex);
    		list_of_emails = list_of_emails + " " + next_email;
    		// update variables
    		i = endIndex + 1;
    		is_email = false;
			window.alert(i);
    	}
    	// next substring separated by space is password
    	else{
    		var endIndex = i + filecontent.substring(i,filecontent.length).indexOf(" ");
    		var next_password = filecontent.substring(i,endIndex);
    		list_of_passwords = list_of_passwords + " " + next_password;
    		// update variables
    		i = endIndex + 1;
    		is_email = true;
			window.alert(i);
    	}
    }
    // update the email that will pass to the server
    document.getElementById("email").value= email + " " + list_of_emails;
    // update the password that will pass to the server
    document.getElementById("password").value= password + " " + list_of_passwords;
    window.alert(document.getElementById("email").value);
    window.alert(document.getElementById("password").value);
    document.getElementById("regForm").submit();
}