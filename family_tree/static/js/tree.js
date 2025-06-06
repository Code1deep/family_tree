// static/js/tree.js
// ✅ Importation des modules
import { loadTreeData } from './tree/core.js';
import { zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js'; 
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';
import { drawTree } from "./tree/core.js";  

// ✅ Confirmation de chargement
console.log('✅ tree.js loaded');

// ✅ Pour debug manuel si besoin
window.initD3Tree = initMainD3Tree;

// ✅ Fonction utilitaire : transforme {nodes, edges} → hiérarchie
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

// ✅ Bloc test manuel (ex: drawTree uniquement pour debug)
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📦 DOMContentLoaded → Test manuel drawTree()");
    const data = await fetchTreeData();
    if (data) {
        console.log("🧪 Données de test reçues :", data);
        drawTree(data);
    } else {
        console.warn("⚠️ Aucune donnée reçue pour le test");
    }
});

// ✅ Bloc principal : chargement de l’arbre généalogique
document.addEventListener("DOMContentLoaded", async () => {
    console.log("📦 DOMContentLoaded → Chargement principal de l'arbre");

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

    // ✅ Ajout des événements de contrôle
    document.getElementById("fullscreen-btn")?.addEventListener("click", () => {
        console.log("🖥️ Clic bouton : Plein écran");
        toggleFullscreen(treeContainer);
    });

    document.getElementById("export-png")?.addEventListener("click", () => {
        console.log("📷 Clic bouton : Export PNG");
        exportPNG(treeContainer);
    });

    document.getElementById("export-svg")?.addEventListener("click", () => {
        console.log("📐 Clic bouton : Export SVG");
        exportSVG(treeContainer);
    });

    document.getElementById("search-box")?.addEventListener("input", (e) => {
        console.log("🔍 Recherche en cours :", e.target.value);
        searchNode(e.target.value);
    });

    document.getElementById("center-btn")?.addEventListener("click", () => {
        console.log("🎯 Clic bouton : Centrer arbre");
        centerTree();
    });
});
