
    function getProfilePicture(imageUrl){
        if(!imageUrl)
            return $("<div>").addClass('profile-picture col-8');
        return $("<div>")
        .addClass('profile-picture col-8')
        .css('background-image', 'url(' + imageUrl + ')');
    }

    function getProfileCard(id, imageUrl, name, age, hobbies, liked){
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
            )
            .append(
                $("<small>")
                .addClass('w-100')
                .html('Age: ' + age)
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
                    )
                    .append('<i class="fa-fw far fa-heart"></i><i class="fa-fw fas fa-heart"></i>')
					.click((e) => {$.ajax({
						url:"users/like/"+ id + "/",
						type:"PUT",
						data:{csrfmiddlewaretoken:csrf},
						success: function(response){
							console.log('this was ' + liked)
						}
					})})
                )
            )
        );
    }

    $(document).ready(function(){
        //Load profiles here
        
			$.ajax({
				url:"/users",
				type:"GET",
				success:function(d){
					console.log(d);
					for(let i = 0; i < d.length; i++){
						var ageDifMs = Date.now() - new Date(d[i].date_of_birth);
						var ageDate = new Date(ageDifMs);
						var age = Math.abs(ageDate.getUTCFullYear() - 1970);
						$('#profiles').append(getProfileCard(i+10,d[i].profile_pic, d[i].first_name, age, [d[i].hobbies,'null'], false))
					}
				}
			});
			for(let i = 0; i < 10; i++){
            $('#profiles').append(getProfileCard(i, '', 'Name', 'Age', ['Hobby 1', 'Hobby 2'], Math.random() >= 0.5));
        }
    });