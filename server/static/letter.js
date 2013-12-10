//enables input into shortURL textbox when shorten URL radio is selected
$("#specify").click(function(){
        $("#short").removeAttr("disabled");
})
//disables input into shortURL textbox when autoCreate radio is selected
$("#autoCreate").click(function(){
	$("#short").prop("disabled","disabled");
})

function allLetter()
{
	var radios = document.getElementsByName("URL");
	if(radios[0].checked){
		//auto
		return true;
	}
	else{
		var short = document.forms["thisForm"]["short"];
		var letters = /^[A-Za-z]+$/;
		if(short.value.match(letters))
		{
			return true;
		}
		else
		{
			alert('Please input letters only.');
			return false;
		}
	}
	return true;
};

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

function validPassword()
{
	//make sure passwords match
	var password = document.forms["create"]["password"];
	if(password.value!=document.forms["create"]["password2"])
	{
		alert("Passwords do not match");
		return false;
	}
	//make sure it matches requirements
	if(password.value.length < 6 || password.value.length > 20)
	{
		alert ("Password must be between 6 and 20 characters long.");
		return false;
	}
	return true;
} 
