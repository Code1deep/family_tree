// static/js/tree.js
// ✅ Importation des modules
import { centerTree, exportPNG, exportSVG, searchNode } from './tree/utils.js'; 
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';

import { loadTreeData, drawTree, zoomIn, zoomOut } from './tree/core.js';


console.log('✅ tree.js loaded');
// static/js/tree.js
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

        const finalData = (treeData.nodes && treeData.edges)
            ? convertToHierarchy(treeData)
            : treeData;

        if (!finalData) {
            console.error("❌ Données finales invalides !");
            return;
        }

        drawTree(finalData);
    } catch (error) {
        console.error("❌ Erreur lors du chargement de l’arbre :", error);
    }
});

/**
 * Convertit { nodes, edges } → hiérarchie D3
 */
function convertToHierarchy(data) {
    const { nodes, edges } = data;
    const nodeById = new Map(nodes.map(d => [d.id, { ...d, children: [] }]));

    for (const edge of edges) {
        const parent = nodeById.get(edge.from);
        const child = nodeById.get(edge.to);
        if (parent && child) {
            parent.children.push(child);
        } else {
            console.warn("⚠️ Lien ignoré : parent ou enfant introuvable", edge);
        }
    }

    const allChildren = new Set(edges.map(e => e.to));
    const root = nodes.find(n => !allChildren.has(n.id));

    if (!root) {
        console.error("❌ Aucun nœud racine trouvé !");
        return null;
    }

    console.log("🌳 Racine trouvée :", root);
    return d3.hierarchy(nodeById.get(root.id));
}

/**
 * Affiche l’arbre généalogique avec D3.js
 */
function drawTree(root) {
    console.log("🧠 Affichage avec D3");

    const width = document.getElementById("wrapper").clientWidth;
    const height = document.getElementById("wrapper").clientHeight;

    const svg = d3.select("#wrapper")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const g = svg.append("g").attr("transform", "translate(40,40)");

    const treeLayout = d3.tree().size([width - 100, height - 100]);
    const treeData = treeLayout(root);

    const link = g.selectAll(".link")
        .data(treeData.links())
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3.linkVertical()
            .x(d => d.x)
            .y(d => d.y)
        )
        .attr("stroke", "#ccc")
        .attr("fill", "none");

    const node = g.selectAll(".node")
        .data(treeData.descendants())
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`);

    node.append("circle")
        .attr("r", 20)
        .attr("fill", "#1e90ff");

    node.append("text")
        .attr("dy", 5)
        .attr("text-anchor", "middle")
        .text(d => d.data.first_name || d.data.label || "??");
}
