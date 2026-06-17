const API_URL = 'http://localhost:8000';

// DOM Elements
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menuToggle');
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const formVivienda = document.getElementById('formVivienda');
const listaViviendas = document.getElementById('listaViviendas');
const listaReservas = document.getElementById('listaReservas');
const modal = document.getElementById('modal');
const modalMessage = document.getElementById('modalMessage');
const closeModal = document.querySelector('.close');
const modalEditar = document.getElementById('modalEditar');
const formEditarVivienda = document.getElementById('formEditarVivienda');
const closeModalEditar = document.querySelector('.close-editar');

// Event Listeners
menuToggle.addEventListener('click', toggleMenu);
navItems.forEach(item => item.addEventListener('click', handleNavigation));
formVivienda.addEventListener('submit', handleCreateVivienda);
formEditarVivienda.addEventListener('submit', handleEditarVivienda);
closeModal.addEventListener('click', () => modal.style.display = 'none');
closeModalEditar.addEventListener('click', () => modalEditar.style.display = 'none');
window.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
    if (e.target === modalEditar) modalEditar.style.display = 'none';
});

// Event delegation para botones de viviendas
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-delete-vivienda')) {
        const propertyId = e.target.dataset.id;
        eliminarVivienda(propertyId);
    }
    if (e.target.classList.contains('btn-view-reservas')) {
        const propertyId = e.target.dataset.id;
        verReservas(propertyId);
    }
    if (e.target.classList.contains('btn-edit-vivienda')) {
        const propertyId = e.target.dataset.id;
        abrirEditarVivienda(propertyId);
    }
});

// Load on page load
document.addEventListener('DOMContentLoaded', () => {
    cargarReservas();
    cargarViviendas();
});

// MENU TOGGLE
function toggleMenu() {
    sidebar.classList.toggle('open');
}

// NAVIGATION
function handleNavigation(e) {
    e.preventDefault();
    const pageName = e.currentTarget.dataset.page;

    // Close sidebar on mobile
    sidebar.classList.remove('open');

    // Remove active class from all nav items and pages
    navItems.forEach(item => item.classList.remove('active'));
    pages.forEach(page => page.classList.remove('active'));

    // Add active class to clicked nav item and corresponding page
    e.currentTarget.classList.add('active');
    document.getElementById(pageName).classList.add('active');

    // Reload data for specific pages
    if (pageName === 'dashboard') cargarReservas();
    if (pageName === 'viviendas') cargarViviendas();
}

// CARGAR RESERVAS (Dashboard)
async function cargarReservas() {
    try {
        const response = await fetch(`${API_URL}/api/reservations/`);
        const data = await response.json();

        if (data.success && data.data.length > 0) {
            listaReservas.innerHTML = data.data.map(reserva => {
                const checkIn = new Date(reserva.check_in);
                const checkOut = new Date(reserva.check_out);
                const hoy = new Date();
                const activa = checkIn <= hoy && checkOut >= hoy;

                return `
                    <div class="reserva-card">
                        <div class="reserva-header">
                            <h4 class="reserva-title">${reserva.guest_name}</h4>
                            <span class="reserva-status">${activa ? '🟢 Activa' : '📋 Próxima'}</span>
                        </div>
                        <div class="reserva-info">
                            <div class="reserva-info-row">
                                <span class="reserva-info-label">Código:</span>
                                <span>${reserva.reservation_code}</span>
                            </div>
                            <div class="reserva-info-row">
                                <span class="reserva-info-label">Check-in:</span>
                                <span>${checkIn.toLocaleDateString('es-ES')}</span>
                            </div>
                            <div class="reserva-info-row">
                                <span class="reserva-info-label">Check-out:</span>
                                <span>${checkOut.toLocaleDateString('es-ES')}</span>
                            </div>
                            <div class="reserva-info-row">
                                <span class="reserva-info-label">Huéspedes:</span>
                                <span>${reserva.num_guests}</span>
                            </div>
                            <div class="reserva-info-row">
                                <span class="reserva-info-label">Plataforma:</span>
                                <span>${reserva.platform || '—'}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            listaReservas.innerHTML = '<p class="loading">No hay reservas aún. Crea la primera desde el formulario.</p>';
        }
    } catch (error) {
        listaReservas.innerHTML = '<p class="error">Error al cargar reservas</p>';
        console.error('Error:', error);
    }
}

// CREATE VIVIENDA
async function handleCreateVivienda(e) {
    e.preventDefault();

    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const googleCalendar = document.getElementById('googleCalendar').value;

    try {
        const response = await fetch(`${API_URL}/api/properties/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: nombre,
                address: direccion,
                google_calendar_id: googleCalendar,
            }),
        });

        const data = await response.json();

        if (data.success) {
            showModal('✅ Vivienda creada correctamente');
            formVivienda.reset();
            cargarViviendas();
        } else {
            showModal('❌ Error al crear vivienda');
            console.error(data);
        }
    } catch (error) {
        showModal('❌ Error de conexión con el servidor');
        console.error('Error:', error);
    }
}

// LOAD VIVIENDAS
async function cargarViviendas() {
    try {
        const response = await fetch(`${API_URL}/api/properties/`);
        const data = await response.json();

        if (data.success && data.data.length > 0) {
            listaViviendas.innerHTML = data.data.map(vivienda => `
                <div class="vivienda-card">
                    <h4>🏠 ${vivienda.name}</h4>
                    ${vivienda.address ? `<div class="vivienda-info"><strong>Dirección:</strong> ${vivienda.address}</div>` : ''}
                    <div class="vivienda-info"><strong>Creada:</strong> ${new Date(vivienda.created_at).toLocaleDateString('es-ES')}</div>
                    <div class="vivienda-actions">
                        <button class="btn btn-secondary btn-small btn-edit-vivienda" data-id="${vivienda.id}">✏️ Editar</button>
                        <button class="btn btn-secondary btn-small btn-view-reservas" data-id="${vivienda.id}">📅 Ver Reservas</button>
                        <button class="btn btn-danger btn-small btn-delete-vivienda" data-id="${vivienda.id}">🗑️ Eliminar</button>
                    </div>
                </div>
            `).join('');
        } else {
            listaViviendas.innerHTML = '<p class="loading">No hay viviendas registradas. ¡Crea la primera!</p>';
        }
    } catch (error) {
        listaViviendas.innerHTML = '<p class="error">Error al cargar viviendas</p>';
        console.error('Error:', error);
    }
}

// VER RESERVAS
function verReservas(propertyId) {
    showModal(`📅 Reservas de la vivienda ${propertyId} (próximamente)`);
}

// ELIMINAR VIVIENDA
async function eliminarVivienda(propertyId) {
    if (!confirm('¿Estás seguro de que quieres eliminar esta vivienda?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/properties/${propertyId}`, {
            method: 'DELETE',
        });

        const data = await response.json();

        if (data.success) {
            showModal('✅ Vivienda eliminada');
            cargarViviendas();
        } else {
            showModal('❌ Error al eliminar vivienda');
        }
    } catch (error) {
        showModal('❌ Error de conexión');
        console.error('Error:', error);
    }
}

// EDITAR VIVIENDA
async function abrirEditarVivienda(propertyId) {
    try {
        const response = await fetch(`${API_URL}/api/properties/${propertyId}`);
        const data = await response.json();

        if (data.success) {
            const vivienda = data.data;
            document.getElementById('editPropertyId').value = propertyId;
            document.getElementById('editNombre').value = vivienda.name;
            document.getElementById('editDireccion').value = vivienda.address || '';
            document.getElementById('editGoogleCalendar').value = vivienda.google_calendar_id;

            modalEditar.style.display = 'block';
        } else {
            showModal('❌ Error al cargar vivienda');
        }
    } catch (error) {
        showModal('❌ Error de conexión');
        console.error('Error:', error);
    }
}

async function handleEditarVivienda(e) {
    e.preventDefault();

    const propertyId = document.getElementById('editPropertyId').value;
    const nombre = document.getElementById('editNombre').value;
    const direccion = document.getElementById('editDireccion').value;
    const googleCalendar = document.getElementById('editGoogleCalendar').value;

    try {
        const response = await fetch(`${API_URL}/api/properties/${propertyId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: nombre,
                address: direccion,
                google_calendar_id: googleCalendar,
            }),
        });

        const data = await response.json();

        if (data.success) {
            showModal('✅ Vivienda actualizada correctamente');
            modalEditar.style.display = 'none';
            cargarViviendas();
        } else {
            showModal('❌ Error al actualizar vivienda');
            console.error(data);
        }
    } catch (error) {
        showModal('❌ Error de conexión');
        console.error('Error:', error);
    }
}

// SHOW MODAL
function showModal(message) {
    modalMessage.textContent = message;
    modal.style.display = 'block';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 3000);
}
