$(document).ready(function () {

    $('a').each(function () {
        let loc = window.location.href
        if (($(this).attr('data-fond') === loc.substring(loc.indexOf('&fond=') + 6)) || ($(this).attr('data-fond') === loc.substring(loc.indexOf('?fond=') + 6))) {
            $('.fond-b').find('.is-checked').removeClass('is-checked');
            $(this).addClass('is-checked');
        }

        if ($(this).attr('data-fond')) {
            $(this).on('click', function () {

                let fond = $(this).attr('data-fond')
                if (fond === '0') {
                    if ((loc.indexOf('&fond=') > 0)) {
                        $(this).attr('href', loc.replace(loc.substring(loc.indexOf('&fond=')), ''))
                    } else if ((loc.indexOf('?fond=') > 0)) {
                        $(this).attr('href', loc.replace(loc.substring(loc.indexOf('?fond=')), ''))
                    } else {
                        $(this).attr('href', '')
                    }
                } else if ((loc.indexOf('?') > 0) && (loc.indexOf('?fond=') < 1)) {

                    if (loc.indexOf('&fond=') < 1) {
                        $(this).attr('href', loc + '&fond=' + fond)
                    } else {
                        $(this).attr('href', loc.replace(loc.substring(loc.indexOf('&fond=')), '&fond=' + fond))
                    }
                } else {
                    $(this).attr('href', '?fond=' + fond)
                }
            })
        }
    })
})