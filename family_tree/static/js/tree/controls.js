// static/js/tree/controls.js
import { toggleFullscreen, exportPNG, exportSVG, debounce, centerTree, searchNode } from './utils.js';
//import { searchNode } from './core.js'; // si searchNode y est défini

/**
 * Attache tous les contrôles UI de l’arbre généalogique.
 * @param {Object} params - Paramètres nécessaires.
 * @param {d3.Selection} params.container - Conteneur D3 du SVG principal.
 * @param {d3.Selection} params.svgRoot - Groupe `<g>` D3 contenant l’arbre.
 * @param {HTMLElement} params.svgNode - Élément DOM <svg>.
 * @param {Object} params.root - Donnée racine D3 (utilisée dans update()).
 * @param {Function} [params.update] - Fonction d’update D3 facultative.
 */
export function setupTreeControls({ container, svgRoot, svgNode, root, update }) {
    if (!svgNode) {
        console.error("❌ Aucun SVG trouvé pour les actions");
        return;
    }

    const parentElement = svgNode.parentElement;

    // 🔘 Centrage
    d3.select("#centerBtn").on("click", () => {
        centerTree(svgRoot, parentElement);
    });

    // 📤 Export PNG
    d3.select("#pngBtn").on("click", () => {
        exportPNG(svgNode);
    });

    // 📤 Export SVG
    d3.select("#svgBtn").on("click", () => {
        exportSVG(svgNode);
    });

    // ⛶ Plein écran
    d3.select("#fullscreenBtn").on("click", () => {
        toggleFullscreen(container.node());
    });

    // 🔍 Recherche (D3)
    d3.select("#treeSearch").on("input", function () {
        searchNode(this.value, svgRoot);
    });

    // ↻ Mise à jour initiale
    if (typeof update === 'function') {
        update(root);
    }

    // 📍 Centrage initial
    setTimeout(() => {
        centerTree(svgRoot, parentElement);
    }, 500);
}

/**
 * Recherche générique via DOM (alternative simple sans D3).
 * Utilisée si les nœuds ont `.node` et `textContent`.
 */
export function setupDOMSearchHighlight() {
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
}
