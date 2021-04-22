$(function (){

     var nowUsername = document.getElementById('nowUsername');
     var show = document.getElementById('showNotification');
     var proc = document.getElementById('procText');
     var statusEvent = document.getElementById('statusEvent');

     //Username
     var currentName = document.getElementById('currentName');
     var newName = document.getElementById('newUserName');
     var pass = document.getElementById('userCurrentPs');

     //FullName
     var currentFullName = document.getElementById('currentFullName');
     var newFirstName = document.getElementById('newFirstname');
     var newLastName = document.getElementById('newLastname');
     var fullPassword = document.getElementById('fullPassword');

     //Email
     var currentEmail = document.getElementById('currentEmails');
     var newEmail = document.getElementById('newEmail');
     var emailPassword = document.getElementById('emailPassword');

     //Password
     var currentEmailPassword = document.getElementById('currentEmailPassword');
     var currentPassword = document.getElementById('currentPassword');
     var newPassword = document.getElementById('newPassword');


     $("button.changeName").click(function (){
       var nesne = $(this);
       var token = nesne.attr("token");

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
                newName.value = "";
                pass.value = "";
                statusEvent.innerText = "başarıyla değiştirildi!";
           },
               error: function (response) {
               statusEvent.innerText = "Güncellemesi başarısız oldu";
            }
       })
       }
    });
     $("button.changeFullName").click(function (){
         var nesne = $(this);
         var token = nesne.attr("token");
         fullname = newFirstname.value+" "+newLastname.value;
         if (currentFullName.value == fullname){
           alert("Yeni Ad Soyad eskisi ile aynı olamaz!");
           newFirstname.value = "";
           newLastname.value = "";
           fullPassword.value = "";
        }
         else{
             $.ajax({
           url:"../fullnamechange",
           data:{
               'currentFullName':currentFullName.value,
               'newFirstName':newFirstName.value,
               'newLastName':newLastName.value,
               'fullPassword':fullPassword.value,
               'csrfmiddlewaretoken': token,
           },
           type:"post",
           dataType:"json",
           success:function(response){
               var fullname = response["fullname"];
                currentFullName.value = fullname;
                newFirstName.value = "";
                newLastName.value = "";
                fullPassword.value = "";
                document.querySelector('#showNotification').classList.remove('d-none');
                document.querySelector('#showNotification').classList.add('d-block');
                document.querySelector('#fullname-change-container').classList.remove('d-block');
                document.querySelector('#fullname-change-container').classList.add('d-none');
                proc.innerText = "Ad Soyad";
                statusEvent.innerText = "başarıyla değiştirildi!";
           },
               error: function (response) {
               statusEvent.innerText = "Güncellemesi başarısız oldu";
            }
          })
         }
     });
     $("button.changeEmail").click(function (){
         var nesne = $(this);
         var token = nesne.attr("token");
         if (currentEmail.value == newEmail.value){
           alert("Yeni Email eskisi ile aynı olamaz!");
           newEmail.value = "";
           emailPassword.value = "";
        }
         else{
             $.ajax({
           url:"../emailchange",
           data:{
               'currentEmail':currentEmail.value,
               'newEmail':newEmail.value,
               'emailPassword':emailPassword.value,
               'csrfmiddlewaretoken': token,
           },
           type:"post",
           dataType:"json",
           success:function(response){
                var email = response["email"];
                currentEmail.value = email;
                newEmail.value = "";
                emailPassword.value = "";
                document.querySelector('#showNotification').classList.remove('d-none');
                document.querySelector('#showNotification').classList.add('d-block');
                document.querySelector('#email-change-container').classList.remove('d-block');
                document.querySelector('#email-change-container').classList.add('d-none');
                proc.innerText = "E-posta";
                statusEvent.innerText = "başarıyla değiştirildi!";
           },
               error: function (response) {
               statusEvent.innerText = "Güncellemesi başarısız oldu";
            }
          })
         }
     });
     $("button.changePassword").click(function (){
         var nesne = $(this);
         var token = nesne.attr("token");
         if (currentEmailPassword.value == newPassword.value){
           alert("Yeni Şifre eskisi ile aynı olamaz!");
           currentEmailPassword.value = "";
           newPassword.value = "";
        }
         else{
             $.ajax({
           url:"../passwordchange",
           data:{
               'currentEmailPassword':currentEmailPassword.value,
               'currentPassword':currentPassword.value,
               'newPassword':newPassword.value,
               'csrfmiddlewaretoken': token,
           },
           type:"post",
           dataType:"json",
           success:function(response){
                var email = response["email"];
                currentEmailPassword.value = currentPassword.value;
                currentPassword.value = "";
                newPassword.value = "";
                document.querySelector('#showNotification').classList.remove('d-none');
                document.querySelector('#showNotification').classList.add('d-block');
                document.querySelector('#password-change-container').classList.remove('d-block');
                document.querySelector('#password-change-container').classList.add('d-none');
                proc.innerText = "Şifre";
                statusEvent.innerText = "başarıyla değiştirildi!";
           },
               error: function (response) {
               statusEvent.innerText = "Güncellemesi başarısız oldu";
            }
          })
         }
     });
})
