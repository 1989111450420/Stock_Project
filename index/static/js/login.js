$(function(){
	$("#uphone").blur(function(){
		if($(this).val() == ""){
			$("#uphone_err").html("手機號不能為空");
			$("#uphone_err").css("color", "red");
		}else{
			$("#uphone_err").html("")
		}
	})
})