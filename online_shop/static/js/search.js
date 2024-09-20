$(document).ready(function() {
    const ajaxSearchUrl = $('#urls').data('ajax-search-url');

    let currentPage = 1;
    let query = '';

    $('#search-input').on('keyup', function() {
        query = $(this).val();
        currentPage = 1;
        performSearch(query, currentPage, ajaxSearchUrl);
    });

    $('#load-more').on('click', function() {
        currentPage++;
        performSearch(query, currentPage, ajaxSearchUrl);
    });

    function performSearch(query, page, ajaxSearchUrl) {
        if (query.length > 1) {
            $.ajax({
                url: ajaxSearchUrl,
                data: { query: query, page: page },
                success: function(data) {
                    let results = data.results;
                    let suggestionsList = $('#suggestions-list');

                    if (page === 1) {
                        suggestionsList.empty();
                    }

                    results.forEach(result => {
                        let listItem = `
                            <li class="d-flex align-items-center p-2 border-bottom">
                                <img src="${result.image_url}" alt="Product Image" class="me-2" style="width: 40px; height: 40px; border-radius: 5px;">
                                <div class="product-info">
                                    <span class="product-name"><a href="${result.url}">${result.name}</a></span>
                                    <span class="category-name"><a href="${result.category_url}">${result.category}</a></span>
                                    <span class="category-name text-muted">${result.article_number}</span>
                                    <span class="product-price text-primary">${result.price} руб.</span>
                                </div>
                            </li>
                        `;
                        suggestionsList.append(listItem);
                    });

                    if (results.length === 0 && page === 1) {
                        suggestionsList.append('<li class="text-muted text-center p-2">Ничего не найдено.</li>');
                    }

                    if (data.has_more) {
                        $('#load-more').show();
                    } else {
                        $('#load-more').hide();
                    }

                    $('#suggestions').show();
                }
            });
        } else {
            $('#suggestions').hide();
        }
    }
});
