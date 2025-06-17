// static/js/tree/tree.js
// ✅ Importation des modules
import { renderFamilyTree } from '/static/js/tree/core.js';
import { toggleFullscreen, exportAsPNG, exportSVG, centerTree, searchNode } from '/static/js/tree/utils.js';
import { openModal } from '/static/js/modal.js';
import { initMainD3Tree, initSubD3Tree } from '/static/js/tree/index.js';  // Ajout setupCenterButton
import { loadTreeData, drawTree, zoomIn, zoomOut } from '/static/js/tree/core.js';
import { setupCenterButton } from '/static/js/tree/d3-tree.js';
console.log("✅ tree.js chargé depuis : ", import.meta.url);

window.initD3Tree = initMainD3Tree;

// 👉 Utilisé si nécessaire pour un autre traitement (pas pour drawTree directement)
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
    const rootNode = data.nodes.find(n => !allChildIds.has(n.id));
    if (!rootNode) {
        console.error("❌ Racine introuvable");
        return null;
    }

    console.log("✅ Racine trouvée :", rootNode);
    return nodeById[rootNode.id];
}
// window.skipAutoInit = true;

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
        const { svg, g, zoom } = await renderFamilyTree("wrapper", treeData);
        console.log("✅ Arbre affiché avec succès");

        // Conversion hiérarchie si besoin
        const hierarchy = convertToHierarchy(treeData);
        if (hierarchy) {
            console.log("✅ Hiérarchie prête :", hierarchy);
        }

        // Boutons
        document.getElementById("fullscreenBtn")?.addEventListener("click", () => {
            toggleFullscreen(treeContainer);
        });

        document.getElementById("pngBtn")?.addEventListener("click", () => {
            exportAsPNG("wrapper");
        });

        document.getElementById("svgBtn")?.addEventListener("click", () => {
            exportSVG(treeContainer);
        });

        document.getElementById("centerBtn")?.addEventListener("click", () => {
            centerTree(svg, g, zoom);
        });

        document.getElementById("treeSearch")?.addEventListener("input", (e) => {
            searchNode(e.target.value, d3.select("svg"));
        });

    } catch (err) {
        console.error("❌ Erreur lors du chargement de l’arbre :", err);
    }
});
