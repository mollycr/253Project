//enables checks the radio button when you click in the textbox
$("#short").click(function(){
	$('#specify').prop('checked', true);
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
	var confirmpassword = document.forms["create"]["password2"]

	//ensure both passwords entered are a match
	if(password.value!=document.forms["create"]["password2"])
	
	{
		alert("Passwords do not match");
		return false;
	}
	//make sure it matches length requirements//
	if (password.value.length < 8)	{
		alert ("Password must be at least 8 characters long.");
		password.focus();
		return false;
	}
	//ensure pw is not same as email//
	if (password.value == email.value){
		alert ("You cannot use your email as your password.");
		return false;
	}
	//ensure pw is not same as username//
	if (password.value == username.value) {
		alert ("You cannot use your username as your password.");
		return false;
	}
	//Some code taken from http://www.the-art-of-web.com/javascript/validate-password///
	//ensure pw includes lowercase character//
	re = /[a-z]/;
	if (!re.test(password.value)) {
		alert ("Your password must contain at least one lowercase letter.");
		password.focus();
		return false;
	}
	//ensure pw includes digit//
	re = /[0-9]/;
	if (!re.test(password.value)) {
		alert ("Your password must contain at least one number.");
		password.focus();
		return false;
	}
	//ensure pw includes uppercase character//
	re = /[A-Z]/;
	if (!re.test(password.value)) {
		alert ("Your password must contain at least one uppercase letter.");
		password.focus();
		return false;
	} 
		
	
	var reEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if (reEmail.test(email.value) != True ) {
		alert ("You must enter a valid email.");
		email.focus();
		return false;
	}
	//if all conditions are met, this is a valid pw//
	return true;
*/

} 
