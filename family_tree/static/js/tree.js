// static/js/tree.js
import { loadTreeData, drawTree, zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js';
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';

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

// ✅ DOMContentLoaded UNIQUE
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📦 DOMContentLoaded → Initialisation");

    const treeContainer = document.getElementById("tree-container");
    if (!treeContainer) {
        console.error("❌ Échec : élément #tree-container introuvable");
        return;
    }

    try {
        console.log("📡 Requête vers /api/tree/ ...");
        const response = await fetch("/api/tree/");
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const treeData = await response.json();
        console.log("✅ Données reçues depuis API :", treeData);

        const finalData = (treeData.nodes && treeData.edges)
            ? convertToHierarchy(treeData)
            : treeData;

        if (!finalData) {
            console.error("❌ Données finales invalides !");
            return;
        }

        console.log("🌳 Initialisation de l’arbre D3.js ...");
        initMainD3Tree("tree-container", finalData);
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
        searchNode(e.target.value);
    });

    document.getElementById("centerBtn")?.addEventListener("click", () => {
        console.log("🎯 Clic bouton : Centrer arbre");
        centerTree();
    });
});
