// Función para obtener y renderizar los productos
function obtenerYRenderizarProductos() {
    const URL = "http://127.0.0.1:5000/productos";

    // Realizamos la solicitud GET al servidor para obtener todos los productos
    fetch(URL)
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                // Si hubo un error, lanzar explícitamente una excepción
                // para ser "catcheada" más adelante
                throw new Error('Error al obtener los productos.');
            }
        })
        .then(function (data) {
            renderizarProductosEnTabla(data);
        })
        .catch(function (error) {
            // En caso de error
            alert('Error al obtener los productos.');
            console.error('Error:', error);
        });
}

// Función para renderizar los productos en la tabla
function renderizarProductosEnTabla(data) {
    let tablaProductos = document.getElementById('tablaProductos');

    // Limpiamos la tabla antes de agregar nuevos productos
    tablaProductos.innerHTML = '';

    // Iteramos sobre los productos y agregamos filas a la tabla
    for (let producto of data) {
        let fila = document.createElement('tr');
        fila.innerHTML =
            '<td>' + producto.titulo + '</td>' +
            '<td align="right">' + producto.categoria_nombre + '</td>' +
            '<td align="right">' + producto.precio + '</td>' +
            '<td><img src=static/img/' + producto.imagen_url + ' alt="Imagen del producto" style="width: 100px;"></td>' +
            '<td align="right"><button>' + 'Agregar' + '</button></td>';

        // Una vez que se crea la fila con el contenido del producto, se agrega a la tabla utilizando el método appendChild del elemento tablaProductos.
        tablaProductos.appendChild(fila);
    }
}

// Asegurémonos de que el DOM esté completamente cargado antes de agregar el evento de clic
document.addEventListener('DOMContentLoaded', function () {
    // Añadimos un evento de clic al botón
    let botonLista = document.getElementById('boton-todos');
    if (botonLista) {
        botonLista.addEventListener('click', function () {
            console.log('Clic en el botón');
            obtenerYRenderizarProductos();
        });
    } else {
        console.error('Elemento con ID "boton-todos" no encontrado.');
    }
});
