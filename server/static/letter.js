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



function validPasswordEmail()
{
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
		alert("empty password");
		//password.focus();//
		//problem = true;
		return false;
		}	
}

	//ensure both passwords entered are a match
//	if (password.value != password2.value){
	//	console.log("reached password match validation");
//		alert("passwords don't match!");
		//problem = true;
//		return false;
//	}

	//make sure it matches length requirements//
	if (password.value.length < 8)	{
		alert("password must be 8 chars");
		console.log("reached length req check");
		//password.focus();
		//problem = true;
		//passwordError.show;
		return false;
	}
/*
	//ensure pw is not same as email//
	if (password.value == email.value){
		console.log ("reached email-password check");
		problem = True;
		otherError.show;
	}
	//ensure pw is not same as username//
	if (password.value == username.value) {
		console.log("reached username-password check");
		problem = True;
		otherError.show;
	}
	//Some code taken from http://www.the-art-of-web.com/javascript/validate-password///
	//ensure pw includes lowercase character//
	re = /[a-z]/;
	if (!re.test(password.value)) {
		console.log("reached a-z check");
		password.focus();
		problem = True;
		passwordError.show;
	}
	//ensure pw includes digit//
	re = /[0-9]/;
	if (!re.test(password.value)) {
		console.log("reached digit validation");
		password.focus();
		problem = True
		passwordError.show;
	}
	//ensure pw includes uppercase character//
	re = /[A-Z]/;
	if (!re.test(password.value)) {
		console.log("reached A-Z check");
		password.focus();
		problem = True;
		passwordError.show;

	} 
		
	
	var reEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if (reEmail.test(email.value) != True ) {
		console.log("reached email validation");
		email.focus();
		problem = True;
		emailError.show;
		
	}

	if (problem == True) {
		return false;
	}

	//if all conditions are met, this is a valid pw//

	//javascript to display hidden values on create_account
	
	return false;
} */
