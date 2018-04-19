function validate() {
	var Result = true;
	var SqlText = $(".sql_text").val();
	var DbName = $(".db_name").val();

	if ( SqlText === null || SqlText.trim() === "" ) {
		alert("SQL文本不能为空.");
		return Result = false;
	} else if ( DbName === null || DbName.trim() === "" ) {
		alert("请选择数据库.");
		return Result = false;
	}
	return Result;
}


$(".review_btn").click(function(){
	var pathname = location.pathname;

	if (pathname == '/workflow/mysql/ddl/' || pathname == '/workflow/mysql/orderdetail/ddl/'){
		var ReviewType = 'ddl'
	} else if (pathname == '/workflow/mysql/dml/' || pathname == '/workflow/mysql/orderdetail/dml/'){
		var ReviewType = 'dml'
	}

	if (validate()) {
		$(".review_btn").attr('disabled', true);
		AutoReview(ReviewType);
		$(".review_btn").attr('disabled', false);
	}
});

function AutoReview(url) {
	var SqlText = $(".sql_text");
	var DbName = $(".db_name");


	$.ajax({
		type: "POST",
		url: "/workflow/mysql/autoreview/" + url,
		dataType: "json",
		data: {
			SqlText:SqlText.val(),
			DbName:DbName.val()
		},
		complete: function() {
		},
		success: function (data) {
			if (data.status != -1) {
				var ReviewResult = data.data;
				var html = '';
                var ResultCount = 0;
                //console.warn(ReviewResult[0].sql);
				for (var i=0; i<ReviewResult.length; i++) {
					alertStyle = "alert-success";
					if (ReviewResult[0].result != "") {
						alertStyle = "alert-danger";
					}
                    //console.warn(ReviewResult[i].result);
                    if (ReviewResult[i].result != ''){
                        html += "<pre style='background-color:LightYellow'><font size='2'>"
                        html += ReviewResult[i].sql + "</br><hr />"
                        html += "<font size='2'>" + ReviewResult[i].result + "</pre>"
                        ResultCount += 1
                    }
				}
                //console.warn(ResultAll);
                if (ResultCount != 0){
                    html = "<pre style='background-color:LightYellow'><font size='3'>校验失败</pre>" + html
                } else {
                    html = "<pre style='background-color:LightGreen'><font size='3'>校验通过</pre>" + html
                    $(".review_btn").addClass('hidden');
                    $(".commit_btn").removeClass('hidden');
                }
				$(".review_result").html(html);
				$(".review_area").removeClass('hidden');

			} else {
				alert("status: " + data.status + "\nmsg: " + data.msg);
			}
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
	});
}
