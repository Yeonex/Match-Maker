function getProfilePicture(imageUrl){
    if(!imageUrl)
        return $("<div>").addClass('profile-picture col-8');
    return $("<div>")
    .addClass('profile-picture col-8')
    .css('background-image', 'url(' + imageUrl + ')');
}

function getProfileCard(id, imageUrl, name, age, gender, hobbies, liked){
    return $("<div>")
    .addClass('col-xl-2 col-lg-3 col-sm-4 col-6 profile-card mb-4')
    .append(
        $("<div>")
        .addClass('card align-items-center text-center')
        .append(
            getProfilePicture(imageUrl)
        )
        .append(
            $("<strong>")
            .addClass('w-100')
            .html(name)
			.css("cursor","pointer")
				.click((e) => {
		$.ajax({
			url:"/users/"+id+"/",
			type:"GET",
			success:function(data){
				if(data.gender === "M"){
					var g = "Male";
				}else{
					var g = "Female";
				}
				$("#user_profile").text(data.first_name + "'s Profile");
				$("#see_user_name").text(data.first_name + " " + data.last_name);
				$("#see_user_gender").text(g);
				$("#see_user_dob").text(data.date_of_birth);
                $("#see_user_hobbies").text(data.hobbies.join(", "));
                if(data.bio == null){
                    bio = "No bio added.";
                }else{
                    bio = data.bio;
                }
                $("#see_user_bio").text(bio);
				if(data.profile_pic){
					$("#user_profile_picture").css("background-image","url("+data.profile_pic+")")
				}
				console.log(data);
				$("#profile_modal").css("backgroundColor","rgba(0,0,0,0.3)");
				$("#profile_modal").show();
			}
		})
		})
        )
        .append(
            $("<small>")
            .addClass('w-100')
            .html(age + ' | ' + gender)
        )
        .append(
            $("<small>")
            .addClass('w-100')
            .html(hobbies.join(", "))
        )
        .append(
            $("<div>")
            .addClass('like')
            .append(
                $("<label>")
                .attr('for', id)
                .append(
                    $("<input>")
                    .attr('type', 'checkbox')
                    .attr('id', id)
                    .prop('checked', liked)
                    .click((e) => {
                        if(e.target !== e.currentTarget)
                            return;
                        $.ajax({
                        url:"users/like/"+ id + "/",
                        type:"PUT",
                        success: function(response){
                            console.log(response);
							var audioElement = document.createElement("audio");
							audioElement.src ="/media/sound/like.ogg";
							console.log('this was ' + liked);
							audioElement.play();
                        },
						error:function(XMLHttpRequest, textStatus, errorThrown){
							console.log(errorThrown)
							var audioElement = document.createElement("audio");
							audioElement.src ="/media/sound/error.ogg";
							audioElement.play();
						}
                    })})
                )
                .append('<i class="fa-fw far fa-heart"></i><i class="fa-fw fas fa-heart"></i>')
            )
        )
    )
    .attr("id", "profile" + id);
}

function getSimilarity(a, b){
    let similar = 0;
    for(let i = 0; i < a.hobbies.length; i++){
        if(b.hobbies.includes(a.hobbies[i]))
            similar ++;
    }
    return similar;
}

$(document).ready(function(){
    window.filtered = undefined;
	$("#profile_modal").css("opacity:0");
	$("#profile_modal").hide();
    //Load profiles here
    $.ajax({
        url:"/users/",
        type:"GET",
        success:function(data){
            console.log(data);
            current_user = data.current_user;
            d = data.others;
            d.sort((a,b)=>{
                return getSimilarity(b, current_user) - getSimilarity(a, current_user);
            });
            for(let i = 0; i < d.length; i++){
                var ageDifMs = Date.now() - new Date(d[i].date_of_birth);
                var ageDate = new Date(ageDifMs);
                var age = Math.abs(ageDate.getUTCFullYear() - 1970);
				d[i].name = d[i].first_name + " " + d[i].last_name;
                $('#profiles').append(getProfileCard(d[i].id,d[i].profile_pic, d[i].name, age, d[i].gender, d[i].hobbies, d[i].liked));
            }
			$("#search").on("keyup", function(){
                var search_res = $(this).val().toLowerCase();
                if(filtered)
                    toCheck = filtered;
                else toCheck = d;
				for(let i = 0; i < toCheck.length; i++){
					if(toCheck[i].name.toLowerCase().includes(search_res)){
						$('#profile'+toCheck[i].id).show();
					}else{
						$('#profile'+toCheck[i].id).hide();
					}
				}
			});
        }
    });
	
	$("#btn-filter").click(function(){
		console.log($("#max_age").val());
		let min = $("#min_age").val();
		let max = $("#max_age").val();
		let gender = $("#gender").val();
		console.log(gender);
		$.ajax({
			url:"/users/?min_age="+min+"&max_age="+max+"&gender="+gender,
			type:"GET",
			success: function(data){
                window.filtered = data.others;
                d = filtered;
                $("#profiles").children().hide();
                search = $('#search').val().toLowerCase();
				for(let i =0; i < d.length; i++){
                    d[i].name=d[i].first_name + ' ' + d[i].last_name;
                    if(d[i].name.toLowerCase().includes(search))
					$("#profile"+d[i].id).show();
				}
			}
		});
	});
	
	$("#cancel").click(function(){
		$("#profile_modal").hide();
	});
});
