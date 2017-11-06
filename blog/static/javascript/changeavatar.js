  function shownew(source) {
    var file = source.files[0];
    if((file.size/1024.0/1024.0)>2)
    {
      alert("It's too big to upload!");
      $("#upload").val("");
      return false;
    }
    if (window.FileReader) {
      if (!/image\/\w+/.test(file.type)) {
        $("#upload").val("");
        alert("We need pictrues!");
        return false;
      }
      var fr = new FileReader();
      fr.onloadend = function(e) {
        document.getElementById("portrait").src = e.target.result;
      };
      fr.readAsDataURL(file);
    }
  }
  function filehint()
  {
  	$("#upload").popover("show");
  }
  function closefilehint()
  {
    $("#upload").popover("hide");
  }
