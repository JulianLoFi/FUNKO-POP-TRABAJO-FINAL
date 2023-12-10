/*============== CARGA DE PRODUCTOS EXISTENTES EN EL CARRITO =================================*/

document.addEventListener('DOMContentLoaded', function () {


    const URL = "http://127.0.0.1:5000/"

    // Función para obtener y renderizar productos
    function obtener_y_renderizar_productos() {
    fetch(URL + 'carrito')
        .then(function (response) {
            if (response.ok) {
                return response.json(); 
            } else {
                throw new Error('Error al obtener los productos.');
            }
        })
        .then(function (data) {
        let tablaCarrito = document.getElementById('tablaCarrito');
        tablaCarrito.innerHTML = '';
        


        // Iteramos sobre los productos y agregamos filas a la tabla
        for (let carrito of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = 
            
                
                '<td>' + carrito.titulo + '</td>' +
                '<td align="right">' + carrito.categoria_nombre + '</td>' +
                '<td align="right">' + carrito.precio + '</td>' +
                // Mostrar miniatura de la imagen
                '<td><img src=static/img/' + carrito.imagen_url +' alt="Imagen del producto" style="width: 100px;"></td>' 
                + '<button class="boton-carrito" data-id="' + carrito.id +'">' + 'COMPRAR AHORA' + '</button>'
                + '<button class="boton-carrito" data-id="' + carrito.id +'">' + 'ELIMINAR COMPRA' + '</button>'
            
            
           
            tablaCarrito.appendChild(fila);
        }
    })
    .catch(function (error) {
        // En caso de error
        alert('Error al agregar el producto.');
        console.error('Error:', error);
    });
    }

    obtener_y_renderizar_productos();
});