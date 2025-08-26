// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    console.log("Página cargada, lista para interacción.");
    // Aquí podrías inicializar alguna función, como cargar dinámicamente el carrito
});

// Agregar producto al carrito usando AJAX
function addToCart(productId) {
    fetch('/add-to-cart/' + productId, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'quantity=1' // ajustable si tienes un input de cantidad
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al agregar al carrito');
        return response.text();
    })
    .then(() => {
        alert('Producto agregado al carrito');
        // Aquí podrías actualizar dinámicamente el número del carrito, por ejemplo
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo agregar el producto al carrito');
    });
}

// Actualizar cantidad de un ítem del carrito
function updateCartQuantity(itemId, quantity) {
    fetch(`/api/v1/carts/items/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al actualizar la cantidad');
        return response.json();
    })
    .then(data => {
        alert('Cantidad actualizada');
        console.log('Actualizado:', data);
        // Podrías recargar solo la sección del carrito si usas componentes dinámicos
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo actualizar la cantidad');
    });
}

// Eliminar ítem del carrito
function removeFromCart(itemId) {
    fetch(`/api/v1/carts/items/${itemId}`, {
        method: 'DELETE',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al eliminar el ítem');
        alert('Ítem eliminado del carrito');
        // Eliminar visualmente el item del DOM (si tienes un id específico en el HTML)
        const itemElement = document.getElementById(`cart-item-${itemId}`);
        if (itemElement) {
            itemElement.remove();
        }
    })
    .catch(error => {
        console.error(error);
        alert('No se pudo eliminar el ítem del carrito');
    });
}
