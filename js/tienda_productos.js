/*========================= CARGA DE PRODUCTOS INICIALES =================================*/

document.addEventListener('DOMContentLoaded', function () {
    
    // URL del servidor
    const URL = "http://127.0.0.1:5000/";

    // Función para obtener y renderizar productos
    function obtenerYRenderizarProductos() {
        fetch(URL + 'productos')
            .then(function (response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error al obtener los productos.');
                }
            })
            .then(function (data) {
                let tablaProductos = document.getElementById('tablaProductos');
                tablaProductos.innerHTML = '';

                // Iteramos sobre los productos y agregamos filas a la tabla
                for (let producto of data) {
                    let fila = document.createElement('tr');
                    fila.innerHTML =
                        '<td>' + producto.titulo + '</td>' +
                        '<td align="right">' + producto.categoria_nombre + '</td>' +
                        '<td align="right">' + producto.precio + '</td>' +
                        '<td><img src=static/img/' + producto.imagen_url + ' alt="Imagen del producto" style="width: 100px;"></td>' +
                        '<td align="right"><button class="agregar-boton" data-id="' + producto.id + '">' + 'Agregar' + '</button></td>';

                    tablaProductos.appendChild(fila);
                }
            })
            .catch(function (error) {
                console.error('Error:', error);
            });
    }

    // Llama a la función al cargar la página
    obtenerYRenderizarProductos();
});
