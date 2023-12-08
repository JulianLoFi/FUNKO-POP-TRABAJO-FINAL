// Función para obtener y renderizar los productos de una categoría
function obtenerYRenderizarProductosPorCategoria(categoria) {
    const URL = `http://127.0.0.1:5000/productos/${categoria}`;

    // Realizamos la solicitud GET al servidor para obtener los productos de la categoría
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

// Asegurar carga del DOM 
document.addEventListener('DOMContentLoaded', function () {
    // Eventos de clic a los botones
    let botonesCategorias = document.querySelectorAll('.boton-lista');
    botonesCategorias.forEach(function (boton) {
        boton.addEventListener('click', function () {
            // Obtén el nombre de la categoría desde el ID del botón
            let categoria = boton.id;
            console.log('Clic en el botón de categoría:', categoria);
            
            // Función para obtener y renderizar productos por categoría
            obtenerYRenderizarProductosPorCategoria(categoria);
        });
    });
});
