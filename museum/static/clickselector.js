$(document).ready(function () {
    $('#categoryMenu').on('click', 'a', function () {
        $('#categoryInput').prop('value', $(this).attr('data-category'));
    })

    $('#formFileMultiple').on('change', function (evt) {
        let tgt = evt.target || window.event.srcElement,
            files = tgt.files;

        if (FileReader && files && files.length) {
            let fr = new FileReader();
            fr.onload = function () {
                $('#basePhoto').attr('src', fr.result)
            }
            fr.readAsDataURL(files[0]);
        } else {
            $('#basePhoto').attr('src', 'static/no_photo.jpg')
        }
    })

    $('label').each(function () {
        if ($(this).attr('for') === 'filesInput') {
            $(this).hide()
        }
        if ($(this).attr('for') === 'photosInput') {
            $(this).hide()
        }
    })

    for (let i = 0; i < 5; i++) {
        $('[name=form-' + i + '-filePhoto]').on('change', function (input) {

        })
    }


    for (let i = 0; i < 5; i++) {
        $('[name=form-' + i + '-filePhoto]').on('change', function (input) {
            let tgt = input.target || window.event.srcElement,
                files = tgt.files;

            if (FileReader && files && files.length) {
                let r = new FileReader();
                let file = input.target.files[0];
                r.readAsDataURL(file)
                r.onload = function (e) {
                    $('#photo-' + i).attr('src', r.result)
                }
            } else {
                $('#photo-' + i).attr('src', '...')
            }
        })
    }
});