$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// dấu $ là một biến, để tham chiếu đến các phần tử trên trang web
$('.plus-cart').click(function () {
    //console.log("Click")
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    //console.log(id)
    $.ajax({
        type: "GET",
        url: "/plus_cart",
        data: {
            prod_id: id
        },
        // statusCode: { 
        //     500: function(response) {
        //        console.log(response)
        //     }
        // }, 
        success: function (data) {
            //console.log(data)
            //console.log('success')
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function () {
    //console.log("Click")
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minus_cart",
        data: {
            prod_id: id
        },
        success: function (data) {

            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            if (eml.disable) {
                $('#minus').addClass('disabled');
                $('#minus').css('pointer-events', 'none');
            } else {
                $('#minus').removeClass('disabled');
                $('#minus').css('pointer-events', 'auto');
            }
        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    //var eml = this.parentNode.children[2]
    var eml = this
    $.ajax({
        type: "GET",
        url: "/remove_cart",
        data: {
            prod_id: id
        },
        success: function (data) {
            //$(eml).closest("tr").fadeOut();
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$('.remove-address').click(function () {
    var id = $(this).attr("id").toString();
    //console.log(id)
    var eml = this
    $.ajax({
        type: "GET",
        url: "/remove_address" ,
        data: {
            id:id,
        },
        success: function (data) {
            console.log("Success")
            // nó tự tìm đến phần tử có ".col-sm-6" để xóa, ảo thật đấy mới biết có dụ này
            eml.closest('.col-sm-6').remove();
        }
    })
})























