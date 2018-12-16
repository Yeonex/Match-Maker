function getProfileCard(picture, name, age, gender, hobbies){
	$("#name").text(name);
	$("#gender").text(gender);
	$("#dob").text(age);
	$("#hobbies").text(hobbies.join(", "));
	if(picture)
		$("#profile-picture").css("background-image","url("+picture+")");
}

$(document).ready(function(){
	$.ajax({
		url:"/users",
		type:"GET",
		success:function(data){
			var d = data.current_user;
			var age = data.current_user.date_of_birth;
			$('#info').append(getProfileCard(d.profile_pic, d.first_name + " " + d.last_name , age, d.gender, d.hobbies));
		}
	});
});
