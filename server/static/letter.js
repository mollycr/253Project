//enables input into shortURL textbox when shorten URL radio is selected
$("#specify").click(function(){
	$("#specify").attr("checked",true);
	$("#autoCreate").attr("checked",false);
//        $("#short").removeAttr("disabled");
});
//disables input into shortURL textbox when autoCreate radio is selected
$("#autoCreate").click(function(){
	//$("#short").prop("disabled","disabled");
	//clears textbox input if somethig was entered
	$("#short").val("");
	$("#specify").attr("checked",false);
	$("#autoCreate").attr("checked",true);
});
$("#short").click(function(){
	$("#specify").attr("checked",true);
	$("#autoCreate").attr("checked",false);
});

function allLetter()
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
		//specify is checked. make sure they have inputted a short URL
		//var short = document.forms["thisForm"]["short"];
		var short=$("#short").val();
		var letters = /^[A-Za-z]+$/;
		if (short==""||short==null){
			alert("Please input a short URL");
			return false;
		}
		else if(short.match(letters))
		{
			return true;
		}
		else
		{
			alert('Please input letters only.');
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
