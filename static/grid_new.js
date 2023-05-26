var buttonFilters = {};
var buttonFilter;
var qsRegex;

var $grid = $('.grid').isotope({
    itemSelector: '.grid-item',
    layoutMode: 'masonry',
    transitionDuration: 0,
    filter: function () {
        var $this = $(this);
        var searchResult = qsRegex ? $this.text().match(qsRegex) : true;
        var buttonResult = buttonFilter ? $this.is(buttonFilter) : true;
        return searchResult && buttonResult;
    },
    getSortData: {
        name: '.name',
        date: '.date'
    },
    sortBy: 'date'
});

var tooltipTriggerList = Array.prototype.slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})


$('.arch-btn-group').on('click', 'a', function () {
    var $this = $(this);
    var $buttonGroup = $this.parents('.arch-btn');
    var filterGroup = $buttonGroup.attr('arch-btn-group');
    buttonFilters[filterGroup] = $this.attr('data-arch');
    buttonFilter = concatValues(buttonFilters);
    $grid.isotope();
});


$('.sort-btn-group').on('click', 'a', function () {
    let sortByValue = $(this).attr('data-sort');
    if (sortByValue === 'date') {
        $grid.isotope({sortBy: 'date', sortAscending: false});
    }
    if (sortByValue === 'date-rev') {
        $grid.isotope({sortBy: 'date', sortAscending: true});
    }
    if (sortByValue === 'name') {
        $grid.isotope({sortBy: 'name', sortAscending: true});
    }
    if (sortByValue === 'name-rev') {
        $grid.isotope({sortBy: 'name', sortAscending: false});
    }
});

$(".sort-btn-group").each(function (i, buttonGroup) {
    var $buttonGroup = $(buttonGroup);
    $buttonGroup.on('click', 'a', function () {
        $buttonGroup.find('.active').removeClass('active');
        $(this).addClass('active');
    });
});

$quicksearch = $('.quicksearch').keyup(debounce(function () {
    qsRegex = new RegExp($quicksearch.val(), 'gi');
    $grid.isotope();
}));

$('.quicksearch').on('click', debounce(function () {
    qsRegex = new RegExp($quicksearch.val(), 'gi');
    $grid.isotope();
}));

window.addEventListener('load', function () {
    $grid.isotope({sortBy: 'date', sortAscending: false});
})

$(".arch-btn-group").each(function (i, buttonGroup) {
    var $buttonGroup = $(buttonGroup);
    $buttonGroup.on('click', 'a', function () {
        $buttonGroup.find('.is-checked').removeClass('is-checked');
        $(this).addClass('is-checked');
    });
});

function concatValues(obj) {
    var value = '';
    for (var prop in obj) {
        value += obj[prop];
    }
    return value;
}

function debounce(fn, threshold) {
    var timeout;
    threshold = threshold || 100;
    return function debounced() {
        clearTimeout(timeout);
        var args = arguments;
        var _this = this;

        function delayed() {
            fn.apply(_this, args);
        }

        timeout = setTimeout(delayed, threshold);
    };
}