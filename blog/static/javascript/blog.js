
  function shownew(source) {
    $("#coverinput").popover("hide");
    var file = source.files[0];
    if((file.size/1024.0/1024.0)>2)
    {
      alert("It's too big to upload!");
      $("#coverinput").val("");
      return false;
    }
    if (window.FileReader) {
      if (!/image\/\w+/.test(file.type)) {
        alert("We need pictrues!");
        $('#newcover').val("");
        return false;
      }
      var fr = new FileReader();
      fr.onloadend = function(e) {
        document.getElementById("cover").src = e.target.result;
      };
      fr.readAsDataURL(file);
    }
  }

  function checkmd(source) {
    $("#markdown").popover("hide");
    file = source.files[0]
    if((file.size/1024.0/1024.0)>5)
    {
      alert("It's too big to upload!");
      $("#markdown").val("");
      return false;
    }
    filename = source.value.substr(source.value.lastIndexOf(".")).toLowerCase();
    if (filename != '.md') {
      alert("We need .md file!");
      $('#markdown').val("");
      return false;
    }
  }

  function add(tag) {
    $("#tags").popover("hide");
    a = tag.value;
    tags = a.split(" ");
    var e = document.getElementById('tags');
    e.innerHTML = '';
    for (var i = 0; i < tags.length; ++i) {
      var span = document.createElement('span');
      span.className = "label label-info";
      span.style = "font-size:15px;";
      var node = document.createTextNode(tags[i]);
      span.appendChild(node);
      var element = document.getElementById('tags');
      element.appendChild(span);
    }
  }

  function thick(img)
  {
    img.style="border:solid;border-color:rgb(186, 187, 182);";
  }

  function thin(img)
  {
    img.style="";
  }
  function filehint()
  {
    $("#coverinput").popover("show");
  }
function mdhint()
{
  $("#markdown").popover("show");
}
function tagshint()
{
  $("#tags").popover("show");
}
