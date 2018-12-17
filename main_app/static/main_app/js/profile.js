//Converts gender value to readable string
function getGender(g){
	if(g === "M"){
		return "Male";
	} else {
		return "Female";
	}
}

//Updates the profile card with the user's information
function getProfileCard(picture, name, age, gender, bio, hobbies){
	$("#name").text(name);
	$("#gender").text(getGender(gender));
	$("#dob").text(age);
	$("#hobbies").text(hobbies.map(function(hobby){return hobby.name}).join(", "));
	if(picture)
		$("#profile-picture").css("background-image","url("+picture+")");
	if(bio === null)
		bio = "No bio added.";
	$("#bio").text(bio);
}

//Toggles the edit form on and off
function toggleEditForm(){
	$("#info").toggle();
	$("#edit-form").toggle();
	if($('#edit').hasClass('edit')){
		//Edit
		$('#edit').removeClass('edit').addClass('cancel').removeClass('btn-primary').addClass('btn-danger');
		$('#first-edit').val(user.first_name);
		$('#last-edit').val(user.last_name);
		$('#gender-edit-info').val(user.gender);
		$('#dob-edit').val(user.date_of_birth);
		for(let i = 0; i < user.hobbies.length; i++){
			$('#hobby'+user.hobbies[i].value).prop('selected', true);
		}
		$("#bio-edit").val(user.bio);
	}else{
		//Cancel
		$('#edit').removeClass('cancel').addClass('edit').addClass('btn-primary').removeClass('btn-danger');
	}
}

$(document).ready(function(){
	//Gets the information about the current user and updates card
	$.ajax({
		url:"/users/current/",
		type:"GET",
		success:function(data){
			window.user = data;
			$('#info').append(getProfileCard(data.profile_pic, data.first_name + " " + data.last_name , data.date_of_birth, data.gender, data.bio, data.hobbies));
		}
	});
	//Gets the list of hobbies for the edit profile form
	$.ajax({
		url:"/users/hobbies/",
		type:"GET",
		success:function(data){
			window.hobbies = data;
			for(var i = 0; i < data.length;i++){
				$("#list-hobbies").append('<option value="' + data[i].value + '" id="hobby' + data[i].value + '">' + data[i].name + "</option>");
			}
		}
	});
	
	//When then edit button is clicked, toggle the form
	$("#edit").click(function(){
		toggleEditForm();
	});
	
	//When the save button is clicked, PUT changes to server, update local text
	$("#save").click(function(){
		let n = $("#first-edit").first().val();
		let l = $("#last-edit").first().val();
		let g = $("#gender-edit-info").val();
		let d = $("#dob-edit").first().val();
		let h = $("#list-hobbies").val();
		let b = $("#bio-edit").val();
		console.log(b);
		let data = $.param({name_0:n,name_1:l,gender:g,date_of_birth:d,bio:b});
		for(let i = 0; i < h.length; i++){
			data += "&hobbies="+h[i];
		}
		$.ajax({
			url:"/users/current/",
			type:"PUT",
			data: data,
			success:function(data){
				toggleEditForm();
				user = data.user;
				getProfileCard(user.profile_pic, user.first_name + ' ' + user.last_name, user.date_of_birth, user.gender, user.bio, user.hobbies);
			}
		});
	});
	
});
