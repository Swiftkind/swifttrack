$(function(){
    $('.global-search-form').submit(function(e){
        e.preventDefault()
    });
    $('.search').keypress(function() {
        var params = {
            type: "POST",
            url: "/management/search/",
            data: {
                'search_text': $('.search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'html',
            success: searchSuccess,
            error: function (xhr) {
                console.log('error:', xhr)
            }
        }
        $.ajax(params);
    });
});

function searchSuccess(data, testStatus, jqXHR) {
    console.log('success')
    $('.search-results').html(data);
}
