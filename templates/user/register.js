function bindCaptchaBtnClick() {
    $("#captchaBtn").on("click", function (event) {
        var $this = $(this)
        //获取email输入框的值，如果没有获取到，给予提示
        var email = $("input[name='email']").val()
        if (!email) {
            alert("请先输入邮箱地址");
        }
        // 通过Ajax发送异步请求
        else {
            $.ajax({
                //要给哪个地址发送请求
                url: "/user/captcha/",
                method: "POST",
                data: {
                    "email": email
                },
                // 请求成功进行回调
                // res获取返回的json
                success: function (res) {
                    var code = res['code']
                    if (code == 200) {
                        // 用户点击发送验证码后取消按钮点击事件
                        $this.off("click")
                        // 开始显示倒计时
                        var countDown = 60;
                        var timer = setInterval(function () {
                            countDown -= 1;
                            if (countDown > 0) {
                                $this.text(countDown + "秒后重新发送");
                            } else {
                                $this.text("获取验证码");
                                // 重新绑定点击事件
                                bindCaptchaBtnClick()
                                //清除定时器
                                clearInterval(timer)
                            }
                        }, 1000);
                        alert("验证码已发送，请注意查收")
                    } else {
                        alert(res['message'])
                    }
                }
            })
        }
    })
}

// 等网页文档所有元素都加载完成后再执行
$(function () {
    bindCaptchaBtnClick();
})
