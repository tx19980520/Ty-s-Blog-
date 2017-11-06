
  function shownew(source) {
    var file = source.files[0];
    if((file.size/1024.0/1024.0)>2)
    {
      alert("It's too big to upload!");
      $("#avatar").val("");
      return false;
    }
    if (window.FileReader) {
      var fr = new FileReader();
      fr.onloadend = function(e) {
        document.getElementById("choose").src = e.target.result;
      };
      fr.readAsDataURL(file);
    }
  }

  function checknickname()
  {
    $("#account").popover('hide');
    var text = document.getElementById("account").value;
    var len1 = 0;
    var len2 = 0;
    for(var i=0;i<text.length;++i)
    {
      var c = text.charCodeAt(i);
      if ((c >= 0x0001 && c <= 0x007e) || (0xff60<=c && c<=0xff9f))
      {
       len1++;
      }
      else{
        len2++;
      }
    }
    if ((len1+len2)<4 && (len1+len2) != 0)
    {
      alert("请输入总共四个字符，可以是汉字、数字或者字母");
    }
  }
  function phonehint()
  {
    $("#phone").popover("show");
  }
  function checkPhone(){
    $("#phone").popover('hide')
    var phone = document.getElementById('phone').value;
    if(phone !='')
    {
      if(!(/^1(3|4|5|7|8)\d{9}$/.test(phone))){
          alert("手机号码有误，请重填");
          return false;
      }
    }
  }
  function attention()
  {
  	$("#account").popover('show');
  }
  function hintone()
  {
  	$("#password").popover("show");
  }
  function checkpassowrd()
  {
    var value = document.getElementById("password").value;
  	$("#password").popover("hide");
    if (value == "")
    {
      return true;
    }
    var regex = /(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}/;
    if(!regex.test(value))
    {
      alert("密码中必须包含字母、数字、特称字符，至少8个字符，最多30个字符");
    }
  }
  function hinttwo()
  {
  	$("#password2").popover('show');
  }
  function checksame()
  {
  	$("#password2").popover("hide");
    var a = document.getElementById('password').value;
    var b = document.getElementById("password2").value;
    if (a != b)
    {
      alert("请保证两次密码一致！")
      $("#password").val("");
      $("#password2").val("");
      return false;
    }
  }
  function filehint()
  {
  	$("#file").popover("show");
  }
  function closefilehint()
  {
    $("#file").popover("hide");
  }
