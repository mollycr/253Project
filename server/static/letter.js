//checks radio button when text clicked
$("#short").click(function(){
        $("#specify").attr('checked', 'checked');
});
$("#autoCreate").click(function(){
	//clears textbox input if somethig was entered
	$("#short").val("");
});

function allLetterNumber()
{
	//var short=$("#short").val();
	//alert($("#autoCreate:checked").val());
	//var radios = document.getElementsByName("URL");
	//if(radios[0].checked){
	
	if ($("#long").val()==""||$("#long").val()==null){
		alert("Please specify a URL to shorten");
		return false;	
	}
	else if($("#autoCreate:checked").val()=="autoCreate"){
		//autocreate is checked
		return true;
	}
	else{ 
		//If button checked for user choice, ensure they have input a short URL
		//var short = document.forms["thisForm"]["short"];
		var short=$("#short").val();
		var letterNumber = /^[A-Za-z0-9]+$/;
		if (short==""||short==null){
			alert("Please input a short URL");
			return false;
		}
		else if(short.match(letterNumber))
		{
			return true;
		}
		else
		{
			alert('Please input letters or numbers only.');
			return false;
		}
	}
}

function validUsername()
{//assuming for the sake of prototyping that we want
//alphanumeric usernames
	var username = document.forms["create"]["username"];
	var alphanum = /^[A-Za-z0-9]+$/;
	if(username.value.match(alphanum))
	{
		return true;
	}
	else
	{
		alert("Invalid username");
		return false;
	}
}

/*Create_account JS*/

function validPasswordEmail()
{
	$("#usernameError").show();
	return false;
/*
	//make sure passwords match//
	var password = document.forms["create"]["password"];
	var email = document.forms["create"]["email"];
	var username = document.forms["create"]["username"];
	var password2 = document.forms["create"]["password2"];
	var passwordError = document.forms["create"]["#passwordField"];
	var emailError = document.forms["create"]["#emailField"];
	var otherError = document.forms["create"]["#otherErrors"];
	var usernameError = document.forms["create"]["#usernameField"]; 
	var problem = false;
	
	//ensure password field filled in
	if (password.value == "" || password.value==null){
		console.log("reached password can't be empty check");
		//alert("empty password");
		//password.focus();//
		//problem = true;
		$("#passwordError").show();
		return false;
	}		
	if (email.value == "" || email.value ==null){
		//alert("empty email");
		//problem = true;	
		$("#emailError").show();
		return false;
	}

	var reEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if (reEmail.test(email.value) != true 	
		//alert("bad email, sucker!");
		//console.log("reached email validation");
		//email.focus();
		problem = true;
		$("#emailError").show();
	}

	//make sure it matches length requirements//
	if (password.value.length < 8)	{
		//alert("password must be 8 chars");
		//console.log("reached length req check");
		//password.focus();
		problem = true;
		$("#passwordError").show();
	}

	//ensure both passwords entered are a match
	if (password.value != password2.value){
	//	console.log("reached password match validation");
		//alert("passwords don't match!");
		problem = true;
		$("#confirmError").show();
	}	

	//ensure pw is not same as email//
	if (password.value == email.value){
		//alert("pw can't be email")
		//console.log ("reached email-password check");
		problem = true;
		$("#pwEmailError").show();
	}

	//ensure pw is not same as username//
	if (password.value == username.value) {
	//	alert("pw can't be username!");
	//	console.log("reached username-password check");
		problem = true;
		$("#pwUsernameError").show();
	
	}

	//Some code taken from http://www.the-art-of-web.com/javascript/validate-password///
	//ensure pw includes lowercase character//
	re = /[a-z]/;
	if (!re.test(password.value)) {
		alert("need a lowercase");
		//console.log("reached a-z check");
		//password.focus();
		problem = true;
		//passwordError.show;
		}

	//ensure pw includes digit//
	re = /[0-9]/;
	if (!re.test(password.value)) {
		alert("need a digit");
	//console.log("reached digit validation");
	//	password.focus();
		problem = true
//		passwordError.show;
		
	}

	//ensure pw includes uppercase character//
	re = /[A-Z]/;
	if (!re.test(password.value)) {
		alert("need an uppercase");
		console.log("reached A-Z check");
		//password.focus();
		problem = true;
		//passwordError.show;
		
	} 
	
/*
	if (problem == true) {
		return false;
	}
	else {
		return true;
	}	
*/
	//if all conditions are met, this is a valid pw//

	//javascript to display hidden values on create_account
}

	return true;
*/

} 
