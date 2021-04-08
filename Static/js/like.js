$(function (){
     $("span.likeBtn").click(function (){
       var nesne = $(this);
       var id = nesne.attr("id");
       var token = nesne.attr("data-token");
       var veri = "id="+id;
       var like = nesne.attr("like");
       if(like == "no"){
           likeObje = document.getElementById(id);
           likeObje.className = 'likeBtn fas fa-thumbs-up fs-4';
           nesne.attr("like","yes");
           likeCount = document.getElementById(id+'-'+id);
           likeCountStrong = document.getElementById(id+'-'+id+'-'+id);
           old = Number(likeCountStrong.textContent);
           old1 = Number(old+1);
           likeCountStrong.textContent = old1;
       }
       else if (like == "yes"){
           likeObje = document.getElementById(id);
           likeObje.className = 'likeBtn far fa-thumbs-up fs-4';
           nesne.attr("like","no");
           likeCount = document.getElementById(id+'-'+id);
           likeCountStrong = document.getElementById(id+'-'+id+'-'+id);
           old = Number(likeCountStrong.textContent);
           if(old == 0){
               likeCountStrong.textContent = Number(old);
           }
           else{
                old = Number(old-1);
               likeCountStrong.textContent = old;
           }
       }


       $.ajax({
           url:"like",
           data:{
               'id':veri,
               'csrfmiddlewaretoken': token,
           },
           type:"post",
           dataType:"json",
           success:function (e){
               alert(e.ok);
           }
       })

    });
})



