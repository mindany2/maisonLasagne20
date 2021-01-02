function change(id)
{
    $.post( "/press_button", {
        javascript_data: id 
    },
    function(data){
        //TODO reload the page without the html
    });
    document.location.reload();
}

function reload()
{
    /*
    var page = document.createElement("div")
    page.style.cssText = "{{manager.get_active_page().get_style()}}"
    var newContent = document.createTextNode('Hi there and greetings!');
      // ajoute le nœud texte au nouveau div créé
    page.appendChild(newContent);
    document.body.appendChild(page)
    */
    // TODO setup all the html

}

window.onload = reload;
