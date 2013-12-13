function validPasswordEmail()
{
	//make sure passwords match//
	var password = $("#password").val();
	var email = $("#email").val();
	var username = $("#username").val();
	var password2 = $("#password2").val();
	var passwordError = $("#passwordField");
	var password2Error = $("#password2Field");
	var emailError = $("#emailField");
	var otherError = $("#otherErrors");
	var usernameError = $("#usernameField"); 

	var problem = false;

	passwordError.hide();
	password2Error.hide();
	emailError.hide();
	otherError.hide();
	usernameError.hide();

	//ensure password field filled in
	if (username==null||username==""){
                usernameError.show();
                problem=true;
        }
	if (password == "" || password==null){
		passwordError.show();
		problem = true;
	}
	if (email == "" || email==null){
		emailError.show();
		problem = true;	
	}
	var reEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if (reEmail.test(email) != true ) {
		emailError.show();
		problem = true;
	}

	//make sure it matches length requirements//
	if (password.length < 8){
		passwordError.show();
		problem = true;
	}

	//ensure both passwords entered are a match
	if (password != password2){
		password2Error.show();
		problem = true;
	}
	//ensure pw is not same as email//
	if (password == email){
		otherError.show();
		problem = true;
	}
	//ensure pw is not same as username//
	if (password == username) {
		otherError.show();
		problem = true;
	}

	//Some code taken from http://www.the-art-of-web.com/javascript/validate-password///
	//ensure pw includes lowercase character//
	re = /[0-9]/;
	if(!re.test(password)) {
		passwordError.show();
		problem = true;
	}
	re = /[a-z]/;
	if(!re.test(password)) {
		passwordError.show();
		problem = true;
	}
	re = /[A-Z]/;
	if(!re.test(password)) {
		passwordError.show();
		problem = true;
	}	

	if (problem == true) {
		problem = false;
		return false;
	}
	else{
		return true;
	}

	//if all conditions are met, this is a valid pw//
}
