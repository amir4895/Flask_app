
$(".trck_btn").click(function() {
    let tracking_number = $(this).closest('tr').find('.trck')[0].innerText;
    let desc = $(this).closest('tr').find('.desc')[0].innerText;
    var traking_info = {
        tracking_number : tracking_number,
        desc :  desc
    }
    $.ajax({
        type : "POST",
        url : '/track',
        dataType: "json",
        data: JSON.stringify(traking_info),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data);
            alert(data)
            },
        error:
            function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus); alert("Error: " + errorThrown);
            }

    });

});


$(".rmv_btn").click(function() {
    let tracking_number = $(this).closest('tr').find('.trck')[0].innerText;
    let desc = $(this).closest('tr').find('.desc')[0].innerText;
    var tracking_info = {
        tracking_number : tracking_number,
        desc :  desc +'!'
    }
    $.ajax({
        type : "POST",
        url : '/remove',
        dataType: "html",
        data: JSON.stringify(tracking_info),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data);
            alert("dsad ");
            },
        error:
            function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus); alert("Error: " + errorThrown);
            }
    });

});