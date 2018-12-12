
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
                )
            )
        );
    }

    $(document).ready(function(){
        //Load profiles here
        for(let i = 0; i < 10; i++){
            $('#profiles').append(getProfileCard(i, '', 'Name', 'Age', ['Hobby 1', 'Hobby 2'], Math.random() >= 0.5));
        }
    });