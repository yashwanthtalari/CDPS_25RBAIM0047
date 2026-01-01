console.log("JS loaded");

// ------------------------------------
// MAP INIT
// ------------------------------------
let map = L.map("map").setView([17.385, 78.4867], 11);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
}).addTo(map);

let selectedMarker = null;
let selectedLat = null;
let selectedLon = null;

// ------------------------------------
// MODE HANDLER
// ------------------------------------
function runMode() {
    const mode = document.getElementById("modeSelect").value;

    if (mode === "gps") {
        getUserLocation();
    } else if (mode === "click") {
        alert("Click on the map to select a location");
    } else {
        runCityTwin();
    }
}

// ------------------------------------
// MAP CLICK
// ------------------------------------
map.on("click", async function (e) {
    if (document.getElementById("modeSelect").value !== "click") return;

    selectedLat = e.latlng.lat;
    selectedLon = e.latlng.lng;

    if (selectedMarker) map.removeLayer(selectedMarker);
    selectedMarker = L.marker([selectedLat, selectedLon]).addTo(map);

    document.getElementById("cityInput").value =
        `${selectedLat.toFixed(6)}, ${selectedLon.toFixed(6)}`;

    runCityTwin();
});

// ------------------------------------
// GPS
// ------------------------------------
function getUserLocation() {
    navigator.geolocation.getCurrentPosition(pos => {
        selectedLat = pos.coords.latitude;
        selectedLon = pos.coords.longitude;

        map.setView([selectedLat, selectedLon], 13);

        if (selectedMarker) map.removeLayer(selectedMarker);
        selectedMarker = L.marker([selectedLat, selectedLon]).addTo(map);

        runCityTwin();
    });
}

// ------------------------------------
// MAIN PIPELINE
// ------------------------------------
async function runCityTwin() {

    if (!selectedLat || !selectedLon) {
        alert("Select a location first");
        return;
    }

    // FLOOD
    const floodRes = await fetch("http://127.0.0.1:8000/flood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            lat: selectedLat,
            lon: selectedLon
        })
    }).then(r => r.json());

    const floodLevel = floodRes.flood_risk === 1 ? "HIGH" : "LOW";

document.getElementById("floodResult").innerHTML = `
  <div class="card flood">
    <h3>🌊 Flood Risk</h3>
    <p><b>Elevation:</b> ${floodRes.elevation} m</p>
    <p><b>Rainfall Index:</b> ${floodRes.rainfall}</p>
    <span class="badge ${floodLevel.toLowerCase()}">${floodLevel}</span>
  </div>
`;


    // HEAT
    const heatRes = await fetch("http://127.0.0.1:8000/heat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            vegetation: [0.1, 0.4, 0.8, 0.2, 0.1],
            builtup: [0.7, 0.3, 0.2, 0.9, 0.8]
        })
    }).then(r => r.json());

    const heatScore = heatRes.risk_layer.reduce((a, b) => a + b, 0);
const heatLevel =
    heatScore >= 3 ? "HIGH" :
    heatScore === 2 ? "MODERATE" : "LOW";

document.getElementById("heatResult").innerHTML = `
  <div class="card heat">
    <h3>🔥 Heat Risk</h3>
    <p><b>Risk Score:</b> ${heatScore}/5</p>
    <span class="badge ${heatLevel.toLowerCase()}">${heatLevel}</span>
  </div>
`;


    // AI
    const aiRes = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            flood: floodRes,
            heat: heatRes
        })
    }).then(r => r.json());

    document.getElementById("aiResult").innerHTML =
        `<pre>${aiRes.recommendations}</pre>`;
}
