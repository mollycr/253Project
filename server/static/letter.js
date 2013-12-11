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
	if(password.value.length < 8)
	{
		alert ("Password must be at least 8 characters long.");
		return false;
	}
	return true;
} 
