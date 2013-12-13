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
	var error = false;
	$(".err").hide();
	if ($("#long").val()==""||$("#long").val()==null){
		//alert("Please specify a URL to shorten");
		error=true;
		$("#noLongLink").show();
	}
	if($("#specify:checked").val()=="specify"){ 
		//If button checked for user choice, ensure they have input a short URL
		var short=$("#short").val();
		var letterNumber = /^[A-Za-z0-9]+$/;
		if (short==""||short==null){
			$("#noShortLink").show();
			var shortError=true;
		}
		else if(short.match(letterNumber))
		{
			return true;
		}
		else
		//short link has characters other than letters and numbers
		{
			$("#shortLinkError").show();
			error=true;
		}
	}
	if(error){
		return false;
	}
	else{
		return true;
	}
}


