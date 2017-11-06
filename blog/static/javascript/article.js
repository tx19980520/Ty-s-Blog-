
  function reply(counter){
  var e = document.getElementById('editcomment');
  e.innerHTML = "reply num "+counter.toString()+":";
  }
function thick(img)
{
img.style="border:solid;border-color:rgb(186, 187, 182);";
}

function thin(img)
{
img.style="";
}
function checkcomment()
{
    var text= document.getElementById("editcomment").value;
    var patt1=new RegExp("<script>");
    if (patt1.test(text))
    {
	    $("#editcomment").val("");
        alert("No way!");
    }
}
