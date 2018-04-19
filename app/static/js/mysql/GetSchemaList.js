var pathname = location.pathname;
if (pathname == '/workflow/mysql/ddl/'){
    GetSchemaList('ddl')
} else if (pathname == '/workflow/mysql/dml/'){
    GetSchemaList('dml')
}

function GetSchemaList(SqlType){
    $.ajax({
        type:'POST',
        url:'/workflow/mysql/schemalist/'+SqlType,
        dataType:'json',
        data:{
            "DbName":$(".db_name").val()
        },
        success:function (data){
            var DbList = data.data
            var $html = ''

            for(var i=0;i<DbList.length;i++){
                $html +='<option value="'+DbList[i]+'">'+DbList[i]+'</option>';
            }
            $('.db_name').append($html)
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}
