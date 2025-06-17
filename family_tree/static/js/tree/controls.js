// static/js/tree/controls.js
import {
  toggleFullscreen,
  exportPNG,
  exportSVG,
  debounce,
  searchNode
} from './utils.js';
import { centerTree } from '/static/js/tree/d3-tree.js';

/**
 * Attache les contrôles de l’arbre généalogique.
 * @param {Object} params - Paramètres nécessaires.
 * @param {d3.Selection} params.container - Conteneur D3 du SVG principal.
 * @param {d3.Selection} params.svgRoot - Groupe `<g>` D3 contenant l’arbre.
 * @param {HTMLElement} params.svgNode - Élément DOM <svg>.
 * @param {Object} params.root - Donnée racine D3.
 * @param {Function} [params.update] - Fonction update() si nécessaire.
 */
export function setupTreeControls({ container, svgRoot, svgNode, root, update }) {
    if (!svgNode) {
        console.error("❌ Aucun élément SVG trouvé.");
        return;
    }

    const parent = svgNode.parentElement;

    const controls = [
        { id: "#centerBtn", handler: () => centerTree(svgRoot, parent) },
        { id: "#pngBtn", handler: () => exportPNG(svgNode) },
        { id: "#svgBtn", handler: () => exportSVG(svgNode) },
        { id: "#fullscreenBtn", handler: () => toggleFullscreen(container.node()) },
        { id: "#treeSearch", handler: function () {
            searchNode(this.value, svgRoot);
        }, type: "input" }
    ];

    for (const ctrl of controls) {
        const el = d3.select(ctrl.id);
        if (!el.empty()) {
            el.on(ctrl.type || "click", ctrl.handler);
        }
    }

    // Exécuter update et centrage initial si fournis
    if (typeof update === "function") update(root);

    setTimeout(() => {
        centerTree(svgRoot, parent);
    }, 500);
}

/**
 * Recherche simple via DOM (optionnelle, alternative à D3).
 */
export function setupDOMSearchHighlight() {
    const input = document.getElementById("tree-search");
    if (!input) return;

    input.addEventListener("input", debounce(() => {
        const query = input.value.trim().toLowerCase();
        document.querySelectorAll("#wrapper .node").forEach(node => {
            const text = node.textContent.toLowerCase();
            node.classList.toggle("node--highlight", query && text.includes(query));
        });
    }, 300));
}
