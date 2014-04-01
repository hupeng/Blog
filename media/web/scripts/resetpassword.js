(function() {
    function reset_password() {
        var form = document.forms[0];
        var email = form.elements['email'].value;
        var newPassword = form.elements['newPassword'].value;
        var confirm = form.elements['confirm'].value;

        if (!email || !newPassword || !confirm) {
            return false;
        }

        if (newPassword != confirm) {
            $("span.error").html("");
            $("div#confirm .error").html("您输入的密码不匹配！");
            return false;
        }

        $.ajax({
            url: "/auth/updatepassword_v2/",
            type: "POST",
            cache: false,
            dataType: "json",
            data: {
                out: "json",
                oldpw: oldPassword,
                newpw: newPassword
            },
            success: function(data) {
                if (data.Result == "SUCCESS") {
                    alert("密码修改成功！");
                    $.ajax({
                        url: "/iphoneorder/order_logout/",
                        dataType: "json",
                        data: {
                            out: "json"
                        },
                        success: function(data) {
                            if (data.Result == "OK") {
                                location.href = "login";
                            }
                        }
                    });
                }else if(data.Result == "FAIL"){
                    if(data.Error == "ERROR_NOT_LOGIN"){
                        $("span.error").html("");
                        $("div#oldPassword .error").html("请先登录！");
                    }

                    if(data.Error == "ERROR_OLDPW_WRONG"){
                        $("span.error").html("");
                        $("div#oldPassword .error").html("原始密码错误。");
                    }
                    
                }
            }
        });
    }

    $("input").bind("focus", function(){
        $("span.error").html("");
    });
    $("input").bind("blur", function(){
        var $this = $(this);
        if(!this.value){
            $("span.error").html("");
            $this.next(".error").html("该值不能为空。");
        }
    });

    $("div.button").bind("click",function(){reset_password();});
})()