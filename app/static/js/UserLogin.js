//回车键提交表单登录
$(document).ready(function() {
	$(document).keydown(function(event) {
		//keycode==13为回车键
		if (event.keyCode == 13) {
			PostUserInfo();
		}
	});
});

$(".login_btn").click(function(){
    if (validate()) {
        PostUserInfo()
    }
});

function validate() {
	var result = true;
	var username = $(".user_name").val();
	var password = $(".user_passwd").val();

	if ( username === null || username.trim() === "" ) {
        alert("用户名不能为空.")
        return result = false;
    } else if ( password === null || password.trim() === "" ) {
        alert("密码不能为空.");
        return result = false;
    }
	return result;
}

function PostUserInfo() {
	var username = $(".user_name");
    var password = $(".user_passwd");

	//将数据通过ajax提交给后端进行检查
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5000/api/v1/userlogin/",
		dataType: "jsonp",
		//dataType: "json",
		data:{
            username: username.val(),
            password: password.val()
		},
		complete: function() {
		},
		success: function(data) {
			//console.warn(data.data);
			//console.warn(username.val());
            if (data.data == "true") {
                $.ajax({
                    type: "POST",
                    url: "/auth/login/",
                    dataType: "json",
                    data: {
                        username: username.val()
                    },
		            complete: function() {
                    },
                    success: function(data) {
						//console.warn("msg:",data.msg);
						//console.warn(data.status)
                        if (data.status == 1) {
				            $(location).attr('href','/workflow/userindex/');
                        }
                        else {
                            alert(data.msg);
                        }
					},
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
						//console.warn("status:",XMLHttpRequest.status);
                        alert(errorThrown);
                    }
                });

			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
		}
	});
}