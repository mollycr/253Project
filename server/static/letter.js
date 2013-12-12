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
	$(".err").hide();
	if ($("#long").val()==""||$("#long").val()==null){
		//alert("Please specify a URL to shorten");
		var longError=true;
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
			var shortError=true;
		}
	}
	if(longError||shortError){
		return false;
	}
	else{
		return true;
	}
}


