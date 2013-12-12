//checks radio button when text clicked
$("#short").focus(function(){
	$("#specify").prop('checked', true);
});

$("#autoCreate").click(function(){
	//clears textbox input if somethig was entered
	$("#short").val("");
	$("#specify").prop('checked', false);
});

function allLetterNumber()
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


