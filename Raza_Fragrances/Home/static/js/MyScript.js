$('.Plus-button').click(function () {
    var id = $(this).attr("pid").toString();
    var elm = this.parentNode.children[1]

    $.ajax({
        type: "GET",
        url:  "/increase-quantity",
        data:{
            Product_id : id
        },
        success: function(data){
            elm.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.total_amount;
        }
    })
})


$('.minus-button').click(function () {
    var id = $(this).attr("pid").toString();
    var elm = this.parentNode.children[1]

    $.ajax({
        type: "GET",
        url:  "/decrease-quantity",
        data:{
            Product_id : id
        },
        success: function(data){
            elm.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total_amount
        }
    })
})


