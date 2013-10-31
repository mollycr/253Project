//function hideCurlies()
    //{
    //find curly brackets and hide them
    //var curlies = /{{}}
    //}

function allLetter()
      { 
      var letters = /^[A-Za-z]+$/;
      if(short.value.match(letters))
      {
      alert('yay! it worked!')
      displayText();
      }
      
       else
      {
      alert('Please input letters only.');
      return false;
      }
      };
      
      
      
 function displayText()
    {
        document.getElementById("url_text").innerHTML="Here's your new short link!";
    };
    
    
    