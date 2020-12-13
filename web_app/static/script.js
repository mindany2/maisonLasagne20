function change(id) // no ';' here
{
    $.post( "/press_button", {
        javascript_data: id 
    },
    function(data){
        document.location.reload();
    });
    
}

