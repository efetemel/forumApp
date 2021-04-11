$(function (){
     $("button.changeName").click(function (){
       var nesne = $(this);
       var token = nesne.attr("token");

       var currentName = document.getElementById('currentName');
       var newName = document.getElementById('newUserName');
       var pass = document.getElementById('userCurrentPs');
       var show = document.getElementById('showNotification');
       var proc = document.getElementById('procText');
       var nowUsername = document.getElementById('nowUsername');

       if (currentName.value == newName.value){
           alert("Yeni Kullanıcı adı eskisi ile aynı olamaz!");
           newName.value = "";
           pass.value = "";
       }
       else if (currentName.value != "" && newName.value !="" && pass.value !=""){
           $.ajax({
           url:"../namechange",
           data:{
               'currentName':currentName.value,
               'newName':newName.value,
               'password':pass.value,
               'csrfmiddlewaretoken': token,
           },
           type:"post",
           dataType:"json",
           success:function(response){
                var newName = response["username"];
                currentName.value = newName;
                document.querySelector('#showNotification').classList.remove('d-none');
                document.querySelector('#showNotification').classList.add('d-block');
                document.querySelector('#name-change-container').classList.remove('d-block');
                document.querySelector('#name-change-container').classList.add('d-none');
                proc.innerText = "Kullanıcı Adı";
                nowUsername.innerText = "@"+newName;
           }
       })
       }
    });
})
