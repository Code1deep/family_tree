// static/js/tree/controls.js
export function initControls(container) {
    // CSS inline
    const style = document.createElement("style");
    style.textContent = `
        #tree-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        .tree-button {
            background: #444;
            color: white;
            border: none;
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 0.9rem;
        }
        .tree-button:hover {
            background: #222;
        }
    `;
    document.head.appendChild(style);

    // Boutons
    const controls = document.createElement("div");
    controls.id = "tree-controls";
    controls.innerHTML = `
        <button class="tree-button" id="centerBtn">Centrer</button>
        <button class="tree-button" id="exportSvgBtn">Exporter SVG</button>
        <button class="tree-button" id="exportPngBtn">Exporter PNG</button>
        <button class="tree-button" id="fullscreenBtn">Plein écran</button>
    `;
    container.before(controls);
}
