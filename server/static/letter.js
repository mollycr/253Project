function allLetter()
{
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
};    
