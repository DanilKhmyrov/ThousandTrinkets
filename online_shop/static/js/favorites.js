$(document).ready(function() {
    const favoriteUrlTemplate = $('#urls').data('favorite-url');

    $('.favorite-button').click(function() {
        var productId = $(this).data('product-number');
        var button = $(this);
        var icon = button.find('i');

        var favoriteUrl = favoriteUrlTemplate.replace('0', productId);

        $.ajax({
            url: favoriteUrl,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.is_favorite) {
                    icon.removeClass('far fa-heart').addClass('fas fa-heart');
                } else {
                    icon.removeClass('fas fa-heart').addClass('far fa-heart');
                }
            }
        });
    });
});
