def get_product_count_text(count):
    if 11 <= count % 100 <= 19:
        return f"{count} товаров"
    else:
        last_digit = count % 10
        if last_digit == 1:
            return f"{count} товар"
        elif 2 <= last_digit <= 4:
            return f"{count} товара"
        else:
            return f"{count} товаров"
