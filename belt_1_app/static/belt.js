// alert('i Was loaded');

// Adding mouse over effect on the ADD Job button
$('#add-color').mouseover(function(){ 
    $(this).css('color', 'blue');
}).mouseout(function(){
    $(this).css('color', 'white');
});

// Adding mouse over effect on the LOGOUT button
$('#logout-color').mouseover(function(){ 
    $(this).css('color', 'red');
}).mouseout(function(){
    $(this).css('color', 'white');
});

//Adding Ajax
$('.pimping_add').submit(function(event){
    //alert('you clicked me');
    event.preventDefault();
    var form = $(this); // Grabbing the form data using the this reference which is a reference of the thing our event is fired from which is in our case the form
    var id = $(this).attr('job_id');

    console.log(form.serialize());

    $.ajax({
        url: `/add_job/${id}`,
        method: 'POST',
        data: form.serialize(),   //$(this).serialize()
        success: function(response){
            console.log(response)
            $('#partial_render').html(response)
        }
    })
})
