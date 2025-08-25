// Inicializar componentes cuando cargue la página
document.addEventListener('DOMContentLoaded', function() {
    console.log("Página cargada, lista para interacción.");
    // Aquí podrías cargar el carrito o productos si quieres
});

// Función para agregar productos al carrito con AJAX
function addToCart(productId) {
    fetch('/api/v1/carts/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al agregar al carrito');
        return response.json();
    })
    .then(data => {
        alert('Producto agregado al carrito');
        // Aquí puedes actualizar el UI, por ejemplo recargar carrito
        console.log('Agregado:', data);
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo agregar el producto al carrito');
    });
}

// Función para actualizar cantidad en el carrito
function updateCartQuantity(itemId, quantity) {
    fetch(`/api/v1/carts/items/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al actualizar la cantidad');
        return response.json();
    })
    .then(data => {
        alert('Cantidad actualizada');
        // Aquí puedes refrescar la vista del carrito
        console.log('Actualizado:', data);
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo actualizar la cantidad');
    });
}

// Función para remover items del carrito
function removeFromCart(itemId) {
    fetch(`/api/v1/carts/items/${itemId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al eliminar el ítem');
        alert('Ítem eliminado del carrito');
        // Aquí refresca el UI para quitar el item eliminado
        console.log('Eliminado itemId:', itemId);
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo eliminar el ítem del carrito');
    });
}
