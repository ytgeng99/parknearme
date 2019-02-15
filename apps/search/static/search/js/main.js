    $('.modal').modal();

    $(document).on('click', '#searchImg', function(e) {
        e.preventDefault();
        var card = $(this).parent();
        var business_id = card.attr('business_id');
        if ($('#' + business_id).length === 0) {
            $.ajax({
                url: '/query_business/' + business_id,
                method: 'GET',
                success: function(res) {
                    $(card).after(res);
                    $(card).next().hide();
                    $(card).next().slideDown(1000);
                }
            });
        }
    });

    $(document).on('click', '#searchCont .name_link', function(e) {
        e.preventDefault();
        var card = $(this).parent().parent().parent();
        var business_id = card.attr('business_id');
        if ($('#' + business_id).length === 0) {
            $.ajax({
                url: '/query_business/' + business_id,
                method: 'GET',
                success: function(res) {
                    $(card).after(res);
                    $(card).next().hide();
                    $(card).next().slideDown(1000);
                }
            });
        }
    });

    $(document).on('click', '.business_photos a', function(e) {
        e.preventDefault();
        var business_photos = $(this).parent().parent();
        $(business_photos).slideUp('slow');
        setTimeout(function() {
            $(business_photos).remove();
        }, 1000);
    });

    $('.card').each(function(i) {
        $(this).delay(200*i).fadeIn(300);
    });

    $(document).on('click', '#lifeSearch a', function(e) {
        e.preventDefault();
        var term = $(this).attr('id');
        var location = $(this).attr('location');
        $('#needsResult').remove();
        $.ajax({
            url: '/needs_search/' + term + '/' + location,
            method: 'GET',
            success: function(res) {
                console.log("res from needs:", res);
                $('#modal1').html(res);
            }
        });
    });