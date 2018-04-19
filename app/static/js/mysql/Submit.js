$(".commit_btn").click(function(){
	var pathname = location.pathname;

	if (pathname == '/workflow/mysql/ddl/' || pathname == '/workflow/mysql/orderdetail/ddl/'){
		var ReviewType = 'ddl'
	} else if (pathname == '/workflow/mysql/dml/' || pathname == '/workflow/mysql/orderdetail/dml/'){
		var ReviewType = 'dml'
	}

	if (ValidateSubmit()) {
		$(".commit_btn").attr('disabled', true);
		SubmitForm(ReviewType);
		$(".commit_btn").attr('disabled', false);
	}
});

function ValidateSubmit() {
	var result = true;
	var OrderTitle = $(".order_title").val();
    var DbName = $(".db_name").val();
    var Auditor = $(".auditor").val()

	if ( OrderTitle === null || OrderTitle.trim() === "" ) {
        alert("工单名称不能为空.")
        return result = false;
    } else if ( DbName === null || DbName.trim() === "" ) {
        alert("请选择数据库.");
        return Result = false;
    } else if ( Auditor === null || Auditor.trim() === "" ) {
        alert("请选择处理人.");
        return result = false;
    }

	return result;
}

function SubmitForm(ReviewType) {
    var OrderTitle = $(".order_title");
    var DbName = $(".db_name");
    var RemarkText = $(".remark_text");
    var SqlText = $(".sql_text");
    var Auditor = $(".auditor");
    var OrderId = $(".order_id");
    var DBASuggest = $(".dba_suggest");
    var NeedBackup = 0;
    if ($(".backup_check").prop('checked')){
        var NeedBackup = 1;
    }

	//将数据通过ajax提交给后端进行检查
	$.ajax({
		type: "POST",
		url: "/workflow/mysql/submit/" + ReviewType,
		dataType: "json",
		data:{
            OrderTitle: OrderTitle.val(),
            DbName: DbName.val(),
            RemarkText: RemarkText.val(),
            SqlText: SqlText.val(),
            Auditor: Auditor.val(),
            OrderId: OrderId.val(),
            DBASuggest: DBASuggest.val(),
            NeedBackup: NeedBackup
		},
		complete: function() {
		},
		success: function(data) {
            if (data.status == -1) {
                alert(data.msg)
            } else {
                alert("提交成功.")
                $(location).attr('href','/workflow/userindex/');
            }
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
		}
	});
}