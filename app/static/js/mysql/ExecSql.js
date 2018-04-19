$(".exec_btn").click(function(){
    var pathname = location.pathname;

    if (pathname == '/workflow/mysql/orderdetail/ddl/'){
        var ReviewType = 'ddl'
    } else if (pathname == '/workflow/mysql/orderdetail/dml/'){
        var ReviewType = 'dml'
    }

    $(".exec_btn").attr('disabled',true);
    ExecDDL(ReviewType);
    $(".exec_btn").attr('disabled',false);

});

function ExecDDL(review_type){
    var SqlText = $(".sql_text");
    var DbName = $(".db_name");
    var OrderId = $(".order_id");
    var NeedBackup = 0;
    if ($(".backup_check").prop('checked')){
        var NeedBackup = 1;
    }

    $.ajax({
        type: "POST",
        url: "/workflow/mysql/execsql/" + review_type,
        dataType: "json",
        data: {
            SqlText: SqlText.val(),
            DbName: DbName.val(),
            OrderId: OrderId.val(),
            NeedBackup: NeedBackup
        },
        complete: function(){
        },
        success: function(data){
            if (data.status != -1) {
                $(location).attr('href','/workflow/userindex/');
            
            } else {
                alert("status: " + data.status + "\nmsg: " + data.msg);
            }

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}