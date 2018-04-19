$(function(){
    $.ajax({
        type:'POST',
        url:'/workflow/dbalist/',
        dataType:'json',
        data:{
            "Auditor":$(".auditor").val()
        },
        success:function (data){
            var DBAList = data.data;
            var $html = '';

            for(var i=0;i<DBAList.length;i++){
                $html +='<option value="'+DBAList[i]+'">'+DBAList[i]+'</option>';
            }
            $('.auditor').append($html)
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
})
