$(document).ready(function() {
    const applyPromoUrl = $('#urls').data('apply-promo');
    const updateCartUrl = $('#urls').data('update-cart-url');
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();

    // Применение промокода
    $('#apply-promo-btn').on('click', function(event) {
        event.preventDefault();
        const promoCode = $('#promo-code-input').val();
        if (promoCode) {
            applyPromoCode(promoCode, applyPromoUrl, csrftoken);
        } else {
            $('#promo-code-message').text('Пожалуйста, введите промокод').show();
        }
    });
    function applyPromoCode(promoCode, applyPromoUrl, csrftoken) {
        $.ajax({
            url: applyPromoUrl,
            type: 'POST',
            data: {
                promo_code: promoCode,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                if (data.success) {
                    $('#total-price').text(data.new_total_price);
                    $('#discount').text('Скидка: ' + data.discount + ' р.');
                    $('#promo-code-applied').text('Промокод применен: ' + promoCode);
                    $('#promo-code-input').hide();
                    $('#apply-promo-btn').hide();
                } else {
                    $('#promo-code-message').text(data.error).show();
                }
            },
            error: function(xhr, status, error) {
                $('#promo-code-message').text('Ошибка при применении промокода.').show();
                console.error(error);
            }
        });
    }

    // Обновление товаров в корзине
    const catalogButtons = $('.add-to-cart-btn');
    catalogButtons.on('click', function() {
        const button = $(this);
        const productId = button.data('product-id');
        const action = button.data('action');
        const quantity = action === 'add' ? 1 : 0;

        updateCart(productId, quantity, csrftoken, updateCartUrl, button);
    });

    const cartButtons = $('.custom-btn-plus, .custom-btn-minus');
    const quantityInputs = $('.item-quantity');

    cartButtons.on('click', function() {
        const productId = $(this).closest('.custom-cart-item').data('product-id');
        const action = $(this).data('action');
        const inputField = $(this).closest('.custom-cart-item').find('.item-quantity');
        let quantity = parseInt(inputField.val());

        if (action === 'add') {
            quantity += 1;
        } else if (action === 'remove' && quantity > 1) {
            quantity -= 1;
        }

        inputField.val(quantity);
        updateCart(productId, quantity, csrftoken, updateCartUrl, null);
    });

    quantityInputs.on('change', function() {
        const productId = $(this).closest('.custom-cart-item').data('product-id');
        let quantity = parseInt($(this).val());
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
        }
        $(this).val(quantity);
        updateCart(productId, quantity, csrftoken, updateCartUrl, null);
    });

    function updateCart(productId, quantity, csrftoken, updateCartUrl, button) {
        $.ajax({
            url: updateCartUrl,
            type: 'POST',
            data: {
                productId: productId,
                quantity: quantity,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                // Обработка успешного запроса
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    // Обновление UI корзины
                    if (button) {
                        if (quantity > 0) {
                            button.text('Удалить');
                            button.data('action', 'remove');
                            button.removeClass('btn-danger').addClass('btn-secondary');
                        } else {
                            button.text('В корзину');
                            button.data('action', 'add');
                            button.removeClass('btn-secondary').addClass('btn-danger');
                        }
                    }

                    $('#total-items').text(data.total_items);
                    $('#total-price').text(data.total_price);

                    const cartItem = $(`[data-product-id="${productId}"]`);
                    cartItem.find('.item-quantity').val(data.item_quantity);
                    const itemPrice = parseFloat(cartItem.find('.custom-cart-item-price').data('price'));
                    updateTotalItemPrice(cartItem, itemPrice, data.item_quantity);
                }
            },
            error: function(xhr) {
                // Если код ошибки 403, перенаправляем на страницу логина
                if (xhr.status === 403 && xhr.responseJSON && xhr.responseJSON.redirect) {
                    window.location.href = xhr.responseJSON.redirect;
                } else {
                    alert('Ошибка при обновлении корзины.');
                }
            }
        });
    }

    function updateTotalItemPrice(cartItem, itemPrice, quantity) {
        const totalItemPrice = cartItem.find('.total-item-price');
        const totalPrice = (itemPrice * quantity).toFixed(1);
        totalItemPrice.text(totalPrice + ' р.');
    }
});
