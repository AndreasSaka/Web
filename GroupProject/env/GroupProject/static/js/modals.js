$(document).ready(function() {
    $('.button-link-modal').click(function(){

        // All product
    
        var productName = $('#product-name');
    
    
    
        productName.html($(this).data('name'));
    
    
    
    });


    $('img').on('click', function() {
        $("#showImg").empty();
        var image = $(this).attr("src");
        $("#showImg").append("<img  class='rounded mx-auto d-block' src='" + image + "' />")
    })
});

