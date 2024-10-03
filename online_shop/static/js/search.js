$(document).ready(function() {
    const ajaxSearchUrl = $('#urls').data('ajax-search-url');
    let currentPage = 1;
    let query = '';

    // Общая функция для обработки поиска
    function performSearch(query, page, ajaxSearchUrl, suggestionsElement, suggestionsListElement, loadMoreButton) {
        if (query.length > 1) {
            $.ajax({
                url: ajaxSearchUrl,
                data: { query: query, page: page },
                success: function(data) {
                    let results = data.results;
                    let suggestionsList = $(suggestionsListElement);

                    if (page === 1) {
                        suggestionsList.empty();
                    }

                    results.forEach(result => {
                        let listItem = `
                            <li class="d-flex align-items-center border-bottom">
                                <img src="https://placehold.co/40x40" alt="Product Image" class="me-2" style="width: 40px; height: 40px; border-radius: 5px;">
                                <div class="product-info">
                                    <span class="product-name"><a href="${result.url}">${result.name}</a></span>
                                    <span class="category-name"><a href="${result.category_url}">${result.category}</a></span>
                                    <span class="category-name text-muted">${result.article_number}</span>
                                    <span class="nav-product-price text-primary">${result.price} руб.</span>
                                </div>
                            </li>
                        `;
                        suggestionsList.append(listItem);
                    });

                    if (results.length === 0 && page === 1) {
                        suggestionsList.append('<li class="text-muted text-center p-2">Ничего не найдено.</li>');
                    }

                    if (data.has_more) {
                        $(loadMoreButton).show();
                    } else {
                        $(loadMoreButton).hide();
                    }

                    $(suggestionsElement).show();
                }
            });
        } else {
            $(suggestionsElement).hide();
        }
    }

    // Обработка поиска для версии ПК
    $('#search-input').on('input', function() {
        query = $(this).val().trim();
        currentPage = 1;

        if (query.length === 0) {
            $('#suggestions').hide();
        } else {
            performSearch(query, currentPage, ajaxSearchUrl, '#suggestions', '#suggestions-list', '#load-more');
        }
    });

    $('#load-more').on('click', function() {
        currentPage++;
        performSearch(query, currentPage, ajaxSearchUrl, '#suggestions', '#suggestions-list', '#load-more');
    });

    // Обработка поиска для мобильной версии
    $('#search-input-mobile').on('input', function() {
        query = $(this).val().trim();
        currentPage = 1;

        if (query.length === 0) {
            $('#suggestions-mobile').hide();
        } else {
            performSearch(query, currentPage, ajaxSearchUrl, '#suggestions-mobile', '#suggestions-list-mobile', '#load-more-mobile');
        }
    });

    $('#load-more-mobile').on('click', function() {
        currentPage++;
        performSearch(query, currentPage, ajaxSearchUrl, '#suggestions-mobile', '#suggestions-list-mobile', '#load-more-mobile');
    });
});
