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
	// get the entered email and password in the form
    var email=document.getElementById("email").value;
    // get the password in the form
    var password=document.getElementById("password").value;
    // remove tailing '\n' character of filecontent
	filecontent = cleanString(filecontent);
	// get the list of emai-password pair in the file
    var lists_of_pairs = filecontent.split(/[\n]/i);
    // extract emails and passwords of students into diferrent variable from filecontent
    var list_of_emails="";
    var list_of_passwords="";
    for(i = 0; i < lists_of_pairs.length; i++){
    	next_pair = lists_of_pairs[i].split(/[^\w\d]/i);
    	// clean up the empty strings in the list
    	next_pair = next_pair.filter(function(n){ return n != undefined && n != "" }); 
    	// default first two string in a line as email and password
    	list_of_emails = list_of_emails + " " + next_pair[0];
    	list_of_passwords= list_of_passwords + " " + next_pair[1];
    }
    // update the email that will pass to the server
    if(email != undefined && password != undefined){
    	list_of_emails = email + " " + list_of_emails;
    	// update the password that will pass to the server
    	list_of_passwords = password + " " + list_of_passwords;
	}
	document.getElementById("email").value = list_of_emails;
	document.getElementById("password").value = list_of_passwords;
	window.alert(document.getElementById("email").value);
    window.alert(document.getElementById("password").value);
    	//document.getElementById("regForm").submit();
}


function cleanString(str){
	while(str.charAt(str.len - 1) == '\n'){
		str = str.substring(0, str.length - 1);
	}
	return str;
}