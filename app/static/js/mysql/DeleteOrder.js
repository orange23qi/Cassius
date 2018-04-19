var pathname = location.pathname;

if (pathname == '/workflow/mysql/orderdetail/ddl/'){
    $(".delete_btn").click(function(){
        DelOrder('ddl')
    });
} else if (pathname == '/workflow/mysql/orderdetail/dml/'){
    $(".delete_btn").click(function(){
        DelOrder('dml')
    });
}

function DelOrder(ReviewType){
    $.ajax({
        type:'POST',
        url:'/workflow/mysql/deleteorder/' + ReviewType,
        dataType:'json',
        data:{
            "OrderId":$(".order_id").val()
        },
        success:function (){
            $(location).attr('href','/workflow/userindex/');
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}
