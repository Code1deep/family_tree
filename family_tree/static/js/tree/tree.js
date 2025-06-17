// static/js/tree/tree.js
// ✅ Importation des modules
import { renderFamilyTree } from '/static/js/tree/core.js';
import { toggleFullscreen, exportSVG, centerTree, searchNode } from '/static/js/tree/utils.js';
import { openModal } from '/static/js/modal.js';
import { exportPNG } from '/static/js/tree/d3-tree.js';
import { initMainD3Tree, initSubD3Tree } from '/static/js/tree/index.js';
import { loadTreeData, drawTree, zoomIn, zoomOut } from '/static/js/tree/core.js';


console.log("✅ tree.js chargé depuis : ", import.meta.url);

console.log('✅ tree.js loaded');
window.initD3Tree = initMainD3Tree;

// Fonction utilitaire
function convertToHierarchy(data) {
    console.log("🔄 Conversion {nodes, edges} → hiérarchie");
    const nodeById = {};
    data.nodes.forEach(n => {
        nodeById[n.id] = { ...n, children: [] };
    });
    data.edges.forEach(e => {
        const parent = nodeById[e.from];
        const child = nodeById[e.to];
        if (parent && child) {
            parent.children.push(child);
        }
    });

    const allChildIds = new Set(data.edges.map(e => e.to));
    const root = data.nodes.find(n => !allChildIds.has(n.id));
    if (!root) {
        console.error("❌ Racine introuvable");
        return null;
    }

    console.log("✅ Racine trouvée :", root);
    return nodeById[root.id];
}

window.skipAutoInit = true;

// ✅ DOMContentLoaded UNIQUE
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📦 DOMContentLoaded → Initialisation");

    const treeContainer = document.getElementById("wrapper");
    if (!treeContainer) {
        console.error("❌ Échec : élément #wrapper introuvable");
        return;
    }

    try {
        console.log("📡 Requête vers /api/tree/ ...");
        const response = await fetch("/api/tree/");
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const treeData = await response.json();
        console.log("✅ Données reçues depuis API :", treeData);

        console.log("🌳 Appel à renderFamilyTree...");
        await renderFamilyTree("wrapper", treeData);
        console.log("✅ Arbre affiché avec succès");

    } catch (err) {
        console.error("❌ Erreur lors du chargement de l’arbre :", err);
    }

    // ✅ Événements UI
    document.getElementById("fullscreenBtn")?.addEventListener("click", () => {
        console.log("🖥️ Clic bouton : Plein écran");
        toggleFullscreen(treeContainer);
    });

    document.getElementById("pngBtn")?.addEventListener("click", () => {
        console.log("📷 Clic bouton : Export PNG");
        exportPNG(treeContainer);
    });

    document.getElementById("svgBtn")?.addEventListener("click", () => {
        console.log("📐 Clic bouton : Export SVG");
        exportSVG(treeContainer);
    });

    document.getElementById("treeSearch")?.addEventListener("input", (e) => {
        console.log("🔍 Recherche en cours :", e.target.value);
        searchNode(e.target.value, d3.select("svg"));
    });

    document.getElementById("centerBtn")?.addEventListener("click", () => {
        console.log("🎯 Clic bouton : Centrer arbre");
        centerTree();
    });
});
