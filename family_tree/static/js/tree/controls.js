// static/js/tree/controls.js
import { toggleFullscreen, exportAsSVG, exportAsPNG } from './utils.js';
import { debounce } from './utils.js';

export function setupTreeControls() {
    const searchInput = document.getElementById('tree-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', debounce(() => {
        const query = searchInput.value.trim().toLowerCase();
        document.querySelectorAll('#tree-container .node').forEach(node => {
            const text = node.textContent.toLowerCase();
            node.classList.remove("node--highlight");
            if (query && text.includes(query)) {
                node.classList.add("node--highlight");
            }
        });
    }, 300));

    // Zooms : à implémenter plus tard
}

document.getElementById('fullscreen-btn').addEventListener('click', () => {
    toggleFullscreen(document.getElementById("tree-container"));
});
document.getElementById('export-svg').addEventListener('click', () => {
    exportAsSVG("tree-container");
});
document.getElementById('export-png').addEventListener('click', () => {
    exportAsPNG("tree-container");
});

export function setupTreeControls() {
    // Zoom buttons
    document.getElementById('zoom-in').addEventListener('click', () => {
        // Logique de zoom
    });

    // Search functionality
    document.getElementById('tree-search').addEventListener('input', (e) => {
        // Recherche dans l'arbre
    });
}
