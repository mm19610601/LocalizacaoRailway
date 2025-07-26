let map;
let markersLayer;
let currentMarkers = [];
let userColors = {};
let heatmapVisible = false;

// Initialize the map
function initMap(locations = []) {
    // Initialize map centered on Portugal
    map = L.map('map').setView([39.5, -8.0], 7);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Create markers layer group
    markersLayer = L.layerGroup().addTo(map);
    
    // Load initial locations
    if (locations.length > 0) {
        updateMapMarkers(locations);
        fitMapBounds();
    }
    
    // Add map controls
    addMapControls();
}

// Update map markers with new data
function updateMapMarkers(locations) {
    // Clear existing markers
    markersLayer.clearLayers();
    currentMarkers = [];
    
    if (locations.length === 0) {
        return;
    }
    
    // Group locations by user for color coding
    const userGroups = {};
    locations.forEach(location => {
        if (!userGroups[location.user_id]) {
            userGroups[location.user_id] = [];
        }
        userGroups[location.user_id].push(location);
    });
    
    // Assign colors to users
    const colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'gray'];
    let colorIndex = 0;
    
    Object.keys(userGroups).forEach(userId => {
        if (!userColors[userId]) {
            userColors[userId] = colors[colorIndex % colors.length];
            colorIndex++;
        }
    });
    
    // Create markers for each location
    locations.forEach(location => {
        const marker = createLocationMarker(location);
        markersLayer.addLayer(marker);
        currentMarkers.push(marker);
    });
    
    // Create user paths
    Object.entries(userGroups).forEach(([userId, userLocations]) => {
        if (userLocations.length > 1) {
            createUserPath(userLocations, userColors[userId]);
        }
    });
    
    // Update statistics
    updateMapStatistics(locations);
}

// Create a marker for a single location
function createLocationMarker(location) {
    const color = userColors[location.user_id] || 'gray';
    
    // Create custom icon
    const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="marker-pin" style="background-color: ${color};">
                   <i class="fas fa-map-marker-alt"></i>
               </div>`,
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -40]
    });
    
    // Create marker
    const marker = L.marker([location.latitude, location.longitude], { icon });
    
    // Create popup content
    const popupContent = createPopupContent(location);
    marker.bindPopup(popupContent);
    
    // Add click event
    marker.on('click', function() {
        highlightUserLocations(location.user_id);
    });
    
    return marker;
}

// Create popup content for a location
function createPopupContent(location) {
    const timestamp = new Date(location.timestamp).toLocaleString('pt-PT');
    const precisao = location.precisao ? `${location.precisao.toFixed(1)}m` : 'N/A';
    
    return `
        <div class="location-popup">
            <h6><i class="fas fa-user me-1"></i>${location.nome_completo || location.username}</h6>
            <hr class="my-2">
            <p class="mb-1">
                <strong><i class="fas fa-map-pin me-1"></i>Coordenadas:</strong><br>
                <code>${location.latitude.toFixed(6)}, ${location.longitude.toFixed(6)}</code>
            </p>
            <p class="mb-1">
                <strong><i class="fas fa-bullseye me-1"></i>Precisão:</strong> 
                <span class="badge bg-secondary">${precisao}</span>
            </p>
            <p class="mb-2">
                <strong><i class="fas fa-clock me-1"></i>Timestamp:</strong><br>
                <small>${timestamp}</small>
            </p>
            <div class="d-grid gap-1">
                <a href="https://www.google.com/maps?q=${location.latitude},${location.longitude}" 
                   target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>Google Maps
                </a>
                <button onclick="centerMapOn(${location.latitude}, ${location.longitude})" 
                        class="btn btn-sm btn-outline-info">
                    <i class="fas fa-crosshairs me-1"></i>Centrar Aqui
                </button>
            </div>
        </div>
    `;
}

// Create path connecting user locations
function createUserPath(locations, color) {
    // Sort locations by timestamp
    const sortedLocations = locations.sort((a, b) => 
        new Date(a.timestamp) - new Date(b.timestamp)
    );
    
    // Create polyline points
    const points = sortedLocations.map(loc => [loc.latitude, loc.longitude]);
    
    // Create polyline
    const polyline = L.polyline(points, {
        color: color,
        weight: 3,
        opacity: 0.6,
        dashArray: '5, 10'
    });
    
    markersLayer.addLayer(polyline);
}

// Highlight all locations for a specific user
function highlightUserLocations(userId) {
    // Reset all marker styles
    currentMarkers.forEach(marker => {
        const markerElement = marker.getElement();
        if (markerElement) {
            markerElement.style.transform = 'scale(1)';
            markerElement.style.zIndex = '1000';
        }
    });
    
    // Highlight markers for the selected user
    currentMarkers.forEach(marker => {
        const popup = marker.getPopup();
        if (popup && popup.getContent().includes(`user_id: ${userId}`)) {
            const markerElement = marker.getElement();
            if (markerElement) {
                markerElement.style.transform = 'scale(1.3)';
                markerElement.style.zIndex = '2000';
            }
        }
    });
}

// Fit map view to show all markers
function fitMapBounds() {
    if (currentMarkers.length === 0) {
        return;
    }
    
    const group = new L.featureGroup(currentMarkers);
    map.fitBounds(group.getBounds().pad(0.1));
}

// Center map on specific coordinates
function centerMapOn(lat, lng, zoom = 15) {
    map.setView([lat, lng], zoom);
}

// Toggle heatmap view
function toggleHeatmap() {
    // This would require implementing a heatmap plugin
    // For now, just show an alert
    alert('Funcionalidade de mapa de calor será implementada em breve');
}

// Add map controls
function addMapControls() {
    // Add scale control
    L.control.scale({
        position: 'bottomright',
        metric: true,
        imperial: false
    }).addTo(map);
    
    // Add custom legend
    const legend = L.control({ position: 'topright' });
    legend.onAdd = function() {
        const div = L.DomUtil.create('div', 'map-legend');
        div.innerHTML = `
            <div class="legend-content">
                <h6><i class="fas fa-info-circle me-1"></i>Legenda</h6>
                <div class="legend-item">
                    <i class="fas fa-map-marker-alt" style="color: red;"></i> Localizações
                </div>
                <div class="legend-item">
                    <i class="fas fa-route" style="color: blue;"></i> Trajetos
                </div>
                <small class="text-muted">Clique nos marcadores para destacar utilizador</small>
            </div>
        `;
        return div;
    };
    legend.addTo(map);
}

// Update map statistics
function updateMapStatistics(locations) {
    // Count unique users
    const uniqueUsers = new Set(locations.map(loc => loc.user_id)).size;
    
    // Calculate time range
    const timestamps = locations.map(loc => new Date(loc.timestamp));
    const timeRange = timestamps.length > 1 ? 
        `${new Date(Math.min(...timestamps)).toLocaleDateString()} - ${new Date(Math.max(...timestamps)).toLocaleDateString()}` :
        'N/A';
    
    // Update UI elements if they exist
    const totalElement = document.getElementById('totalLocations');
    if (totalElement) {
        totalElement.textContent = locations.length;
    }
    
    const recent24hElement = document.getElementById('recent24h');
    if (recent24hElement) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const recentCount = locations.filter(loc => 
            new Date(loc.timestamp) > yesterday
        ).length;
        recent24hElement.textContent = recentCount;
    }
}

// Handle map resize
function resizeMap() {
    if (map) {
        map.invalidateSize();
    }
}

// Export functions for global access
window.initMap = initMap;
window.updateMapMarkers = updateMapMarkers;
window.fitMapBounds = fitMapBounds;
window.centerMapOn = centerMapOn;
window.toggleHeatmap = toggleHeatmap;
window.resizeMap = resizeMap;
