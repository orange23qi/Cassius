$(".reject_btn").click(function(){
    var pathname = location.pathname;
    if(ValidateSuggest()){
        if (pathname == '/workflow/mysql/orderdetail/ddl/'){
            RejectOrder('ddl')
        } else if (pathname == '/workflow/mysql/orderdetail/dml/'){
            RejectOrder('dml')
        }
    }
});

function ValidateSuggest() {
	var Result = true;
	var DBASuggest = $(".dba_suggest").val();

	if ( DBASuggest === null || DBASuggest.trim() === "" ) {
		alert("审核建议不能为空.");
		return Result = false;
	}
	return Result;
}

function RejectOrder(ReviewType){
    var NeedBackup = 0
    if ($(".backup_check").prop('checked')){
        var NeedBackup = 1;
    }     

    $.ajax({
        type:'POST',
        url:'/workflow/mysql/rejectorder/' + ReviewType,
        dataType:'json',
        data:{
            "OrderId":$(".order_id").val(),
            "OrderTitle":$(".order_title").val(),
            "DbName":$(".db_name").val(),
            "RemarkText":$(".remark_text").val(),
            "SqlText":$(".sql_text").val(),
            "OwnerId":$(".owner_id").val(),
            "DBASuggest":$(".dba_suggest").val(),
            "NeedBackup":NeedBackup
        },
        success:function (){
            $(location).attr('href','/workflow/userindex/');
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}
