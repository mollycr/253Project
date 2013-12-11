function selectCustom(){
	//selects custom url when you click on the textbox
	$("#specify").prop("checked", true);	
}
function clearCustom(){
	//clears out the custom url field
	$("#short").val('');
}

function allLetter()
{	
	if ($("#long").val()==""||$("#long").val()==null){
		alert("Please specify a URL to shorten");
		return false;	
	}
	else if($("#autoCreate:checked").val()=="autoCreate"){
		//autocreate is checked
		return true;
	}
	else{ 
		//specify is checked. make sure they have inputted a short URL
		//var short = document.forms["thisForm"]["short"];
		var short=$("#short").val();
		var alphanum = /^[A-Za-z0-9]+$/;
		if (short==""||short==null){
			alert("Please input a short URL");
			return false;
		}
		else if(short.match(alphanum))
		{
			return true;
		}
		else
		{
			alert('Please input letters and numbers only.');
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
	if(password.value.length < 6 || password.value.length > 20)
	{
		alert ("Password must be between 6 and 20 characters long.");
		return false;
	}
	return true;
} 
