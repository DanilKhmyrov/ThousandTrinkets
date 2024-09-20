$(document).ready(function() {
    const updateCartUrl = $('#urls').data('update-cart-url');
    const buttons = $('.custom-btn-plus, .custom-btn-minus');
    const quantityInputs = $('.item-quantity');

    // Обработка кликов по кнопкам + и -
    buttons.on('click', function() {
        const productId = $(this).closest('.custom-cart-item').data('product-id');
        const action = $(this).data('action');
        const inputField = $(this).closest('.custom-cart-item').find('.item-quantity');
        let itemPrice = parseFloat($(this).closest('.custom-cart-item').find('.custom-cart-item-price').data('price'));  // Цена за единицу товара
        let quantity = parseInt(inputField.val());

        // Проверяем корректность itemPrice
        if (isNaN(itemPrice)) {
            itemPrice = 0;
        }

        // Увеличение или уменьшение количества
        if (action === 'add') {
            quantity += 1;
        } else if (action === 'remove' && quantity > 1) {
            quantity -= 1;
        }

        inputField.val(quantity); // Обновляем значение в поле

        const csrftoken = $('[name=csrfmiddlewaretoken]').val();
        updateCart(productId, quantity, csrftoken, updateCartUrl);

        // Пересчитываем и обновляем итоговую цену для товара
        updateTotalItemPrice($(this).closest('.custom-cart-item'), itemPrice, quantity);
    });

    // Обработка изменения количества через поле ввода
    quantityInputs.on('change', function() {
        const productId = $(this).closest('.custom-cart-item').data('product-id');
        let quantity = parseInt($(this).val());
        let itemPrice = parseFloat($(this).closest('.custom-cart-item').find('.custom-cart-item-price').data('price'));  // Цена за единицу товара

        // Проверяем корректность itemPrice
        if (isNaN(itemPrice)) {
            itemPrice = 0;
        }

        // Валидация значения, если введено некорректное число
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
        }

        $(this).val(quantity); // Обновляем значение в поле

        const csrftoken = $('[name=csrfmiddlewaretoken]').val();
        updateCart(productId, quantity, csrftoken, updateCartUrl);

        // Пересчитываем и обновляем итоговую цену для товара
        updateTotalItemPrice($(this).closest('.custom-cart-item'), itemPrice, quantity);
    });

    // Функция пересчета и обновления итоговой цены для товара
    function updateTotalItemPrice(cartItem, itemPrice, quantity) {
        const totalItemPrice = cartItem.find('.total-item-price');
        const totalPrice = (itemPrice * quantity).toFixed(2);  // Рассчитываем новую общую цену
        totalItemPrice.text(totalPrice + ' р.');  // Обновляем текст с новой ценой
    }

    // Функция обновления корзины через AJAX
    function updateCart(productId, quantity, csrftoken, updateCartUrl) {
        $.ajax({
            url: updateCartUrl,
            type: 'POST',
            data: {
                productId: productId,
                quantity: quantity,  // Передаем новое количество
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                $('#total-items').text(data.total_items); // Обновляем общее количество товаров
                $('#total-price').text(data.total_price); // Обновляем общую стоимость

                const cartItem = $(`[data-product-id="${productId}"]`);

                // Обновляем количество товара в поле
                cartItem.find('.item-quantity').val(data.item_quantity);

                // Если количество стало 0, удаляем товар из DOM
                if (data.item_quantity <= 0) {
                    cartItem.remove();
                }
            }
        });
    }
});
