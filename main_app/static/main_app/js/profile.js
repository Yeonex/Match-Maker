function getProfileCard(picture, name, age, gender, hobbies){
	if(gender === "M"){
		gender = "Male";
	} else {
		gender = "Female"
	}
	$("#name").text(name);
	$("#gender").text(gender);
	$("#dob").text(age);
	$("#hobbies").text(hobbies.join(", "));
	if(picture)
		$("#profile-picture").css("background-image","url("+picture+")");
}

$(document).ready(function(){
	$("#first-edit").hide();
	$("#last-edit").hide();
	$("#dob-edit").hide();
	$("#gender-edit").hide();
	$("#gender-edit-info").hide();
	$("#save").hide();
	$("#cancel").hide();
	$("#list_hobbies").hide();
	
	$.ajax({
		url:"/users",
		type:"GET",
		success:function(data){
			window.d = data.current_user;
			var age = data.current_user.date_of_birth;
			$('#info').append(getProfileCard(d.profile_pic, d.first_name + " " + d.last_name , age, d.gender, d.hobbies));
		}
	});
	$.ajax({
		url:"/users/hobbies/",
		type:"GET",
		success:function(data){
			console.log(data);
			for(var i = 0; i < data.length;i++){
				$("#list_hobbies").append("<option value="+data[i].value+">"+data[i].name+"</option>");
			}
		}
	});
	
	$("#edit").click(function(data){
		console.log($("#dob").text());
		$("#edit").hide();
		$("#name").hide();
		$("#first-edit").show();
		$("#first-edit").attr("value",d.first_name);
		$("#last-edit").show();
		$("#last-edit").attr("value",d.last_name);
		$("#dob").hide();
		$("#dob-edit").show();
		$("#dob-edit").attr("value",$("#dob").text());
		$("#gender").hide();
		$("#gender-edit").show();
		$("#gender-edit-info").show();
		$("#save").show();
		$("#cancel").show();
		$("#list_hobbies").show();
		
	});
	
	$("#cancel").click(function(){
		$("#edit").show();
		$("#name").show();
		$("#dob").show();
		$("#gender").show();
		$("#first-edit").hide();
		$("#last-edit").hide();
		$("#save").hide();
		$("#cancel").hide();
		$("#gender-edit").hide();
		$("#gender-edit-info").hide();
		$("#dob-edit").hide();
		$("#list_hobbies").hide();
	});
	
	$("#save").click(function(){
		var n = $("#name-edit").first().val();
		var l = $("name-edit").first().val();
		var g = $("#gender-edit-info").val();
		var d = $("#dob-edit").first().val();
		var h = $("#list_hobbies").val();
		console.log(g);
		$.ajax({
			url:"/profile/",
			put:"PUT",
			data: {name: n, last: l, gender: g, dob: d, hobbies: h},
			success:function(response){
			}
			
			
		});
	});
	
});


