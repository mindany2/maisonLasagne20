function change(id) // no ';' here
{
    var name;
    $.post( "/press_button", {
        javascript_data: id 
    },
    function(data){
        document.location.reload();
    });
    
}

