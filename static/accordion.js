let content = $('.accord-content')
content.attr('style', 'display: none;')

$(document).ready(function () {
    let item = $('.accord-item');
    let trigger = $('.accord-trigger')
    let icon = $('.accord-icon')

    let icon_close = '/static/icons/caret-right-fill.svg'
    let icon_open = '/static/icons/caret-down-fill.svg'

    let category = $('#category').text()

    item.each(function () {
        $(this).children('.accord-content').parent().children(trigger).children(icon).attr('src', icon_close)
        if ($(this).children('.accord-trigger').children('.accord-header').attr('data-category') === category) {
            $('.accord').find('.is-checked').removeClass('is-checked');
            $('#cat-home').removeClass('is-checked');
            $(this).children(trigger).children('.accord-header').addClass('is-checked');
            $(this).parents('.accord-item').each(function () {
                if (parseInt($(this).children('.accord-trigger').children('.accord-header').attr('data-level')) > 0) {
                    $(this).parent().toggle()
                    $(this).parent().parent().children(trigger).children(icon).attr('src', icon_open)
                }
            })
            if (parseInt($(this).children('.accord-trigger').children('.accord-header').attr('data-level')) > 0) {
                $(this).parent().toggle()
                $(this).parent().parent().children(trigger).children(icon).attr('src', icon_open)
            }
        }

    })
    trigger.on('click', function () {
        $(this).next().slideToggle(200);
        if ($(this).children(icon).attr('src') === icon_close) {
            $(this).children(icon).attr('src', icon_open)
        } else if ($(this).children(icon).attr('src') === icon_open) {
            $(this).children(icon).attr('src', icon_close)
        }
    })
})