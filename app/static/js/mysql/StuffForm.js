var pathname = location.pathname;
var IfDBA = "False"

if (pathname == '/workflow/mysql/orderdetail/ddl/'){
    var OrderId = GetOrderId()
    StuffForm("ddl", OrderId)
} else if (pathname == '/workflow/mysql/orderdetail/dml/'){
    var OrderId = GetOrderId()
    StuffForm("dml", OrderId)
}

function ChangeFormFields (NowUser, Owner, Status, IfDBA) {
    if (IfDBA == "True"){
        $(".sql_text").attr("readonly",true);

        $('.owner_area').removeClass('hidden');
        $('.suggest_area').removeClass('hidden');

        $('.auditor_area').addClass('hidden');
        $('.review_area').addClass('hidden');
        $('.dev_btn_area').addClass('hidden');

        if (Status == "DBA审核") {
            $('.review_btn_area').removeClass('hidden');

        } else if (Status == "用户修改") {
            $('.dev_btn_area').removeClass('hidden');
            $('.dba_suggest').attr("readonly",true);
            $('.sql_text').attr("readonly",false);

        } else {
            $('.dba_suggest').attr("readonly",true);

        }

    } else if (NowUser == Owner) {
        $('.suggest_area').removeClass('hidden');
        $('.delete_btn').removeClass('hidden');
        $('.dba_suggest').attr('readonly',true);

        if (Status != "用户修改" ) {
            $('.sql_text').attr('readonly',true);
            $('.dev_btn_area').addClass('hidden');

            if ($('.dba_suggest').val() === null || $('.dba_suggest').val() === ""){
                $('.suggest_area').addClass('hidden');
            }
        }

    } else if (NowUser != Owner && IfDBA == "False"){
        //返回权限界面
    
    }
}

function GetOrderId() {
    var url = location.search; //获取url中"?"符后的字串
    var str = ""

    if (url.indexOf("?") != -1) {
        str = url.substr(1);
    }
    return str
}

function CheckDBA(NowUser, Owner, Status){
    $.ajax({
        type:'GET',
        url:'/workflow/dbalist/',
        dataType:'json',
        success:function (data){
            var DBAList = data.data;

            for(var i=0;i<DBAList.length;i++){
                if (NowUser == DBAList[i]){
                    IfDBA = "True"
                }
            }

            ChangeFormFields(NowUser, Owner, Status, IfDBA)
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}

function StuffForm(ReviewType, OrderId){
    $.ajax({
        type: "GET",
        url: "/workflow/mysql/orderdetail/" + ReviewType +"/" + OrderId,
        dataType: "json",
        complete: function(){
        },
        success: function(data){
            Result = data.data
            OrderTitle = Result[0]
            DbName = Result[1]
            RemarkText = Result[2]
            SqlText = Result[3]
            Status = Result[4]
            Owner = Result[5]
            Auditor = Result[6]
            NowUser = Result[7]
            OrderId = Result[8]
            OwnerId = Result[9]
            DBASuggest = Result[10]

            var pathname = location.pathname;
            
            if (pathname == '/workflow/mysql/orderdetail/dml/'){
                NeedBackup = Result[11]
                if (NeedBackup == 1) {
                    $(".backup_check").prop('checked',true);
                } else {
                    $(".backup_check").prop('checked',false);
                }
            }

            $(".order_title").val(OrderTitle);
            $(".db_name").append('<option value="'+DbName+'" selected="selected">'+DbName+'</option>');
            $(".remark_text").val(RemarkText);
            $(".sql_text").val(SqlText);
            $(".auditor").append('<option value="'+Auditor+'" selected="selected">'+Auditor+'</option>');
            $(".owner").val(Owner);
            $(".order_id").val(OrderId);
            $(".owner_id").val(OwnerId);
            $(".dba_suggest").val(DBASuggest);

            $(".order_title").attr("readonly",true);
            $(".db_name").attr("readonly",true);
            $(".db_name").attr("disabled",true);
            $(".remark_text").attr("readonly",true);
            $(".auditor").attr("readonly",true);
            $(".auditor").attr("disabled",true);
            $(".owner").attr("readonly",true);

            $(".reset_btn").addClass("hidden");

            CheckDBA(NowUser, Owner, Status);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            alert(errorThrown);
        }
    });
}
