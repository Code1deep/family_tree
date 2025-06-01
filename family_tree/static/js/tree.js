// static/js/tree.js
import { loadTreeData } from './tree/core.js';
import { initD3Tree } from './tree/d3-tree.js';
import { initTree, zoomIn, zoomOut, centerTree, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { openModal } from "/static/js/modal.js";

document.addEventListener("DOMContentLoaded", async () => {
  const treeContainer = document.getElementById("tree-container");
  if (!treeContainer) {
    console.error("❌ tree-container introuvable !");
    return;
  }

  try {
    const response = await fetch("/api/person/api/visualize/tree/1");
    const treeData = await response.json();
    console.log("✅ Données reçues :", treeData);
    initD3Tree(treeData);  // ou ta fonction de rendu
  } catch (err) {
    console.error("❌ Erreur lors du chargement de l’arbre :", err);
  }

  // Événements boutons
    document.getElementById("zoom-in-btn").addEventListener("click", zoomIn);
    document.getElementById("zoom-out-btn").addEventListener("click", zoomOut);
    document.getElementById("center-btn").addEventListener("click", centerTree);
    document.getElementById("fullscreen-btn").addEventListener("click", () => toggleFullscreen(treeContainer));
    document.getElementById("export-png-btn").addEventListener("click", () => exportPNG(treeContainer));
    document.getElementById("export-svg-btn").addEventListener("click", () => exportSVG(treeContainer));
    document.getElementById("search-input").addEventListener("input", (e) => searchNode(e.target.value));
});
