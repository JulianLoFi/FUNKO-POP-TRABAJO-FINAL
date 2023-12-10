//==========Agregar productos al clickear "Agregar" =====

const URL = "http://127.0.0.1:5000/"

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('agregar-boton')) {
        const idProducto = event.target.getAttribute('data-id');

        fetch(URL + `/carrito/${idProducto}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            //Recarga la página
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});