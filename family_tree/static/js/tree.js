// static/js/tree.js
// ✅ Chargement des modules
import { loadTreeData } from './tree/core.js';
import { zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js'; 
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';
import { drawTree } from "./tree/core.js";  

// ✅ Confirmation de chargement
console.log('✅ tree.js loaded');

// ✅ Exposition facultative de la fonction pour débogage
window.initD3Tree = initMainD3Tree;

// Pour test uniquement si nécessaire :
document.addEventListener("DOMContentLoaded", async () => {
    const data = await fetchTreeData();
    if (data) {
        drawTree(data);  // <- TEST uniquement
    }
});

document.addEventListener("DOMContentLoaded", async () => {
  const treeContainer = document.getElementById("tree-container");
  if (!treeContainer) {
    console.error("❌ tree-container introuvable !");
    return;
  }

  try {
    const response = await fetch("/api/tree/");
    if (!response.ok) throw new Error(`Erreur HTTP ${response.status}`);
    const treeData = await response.json();
    console.log("✅ Données reçues :", treeData);
    initMainD3Tree("tree-container", treeData);
  } catch (err) {
    console.error("❌ Erreur lors du chargement de l’arbre :", err);
  }

  document.getElementById("fullscreen-btn")?.addEventListener("click", () => toggleFullscreen(treeContainer));
  document.getElementById("export-png")?.addEventListener("click", () => exportPNG(treeContainer));
  document.getElementById("export-svg")?.addEventListener("click", () => exportSVG(treeContainer));
  document.getElementById("search-box")?.addEventListener("input", (e) => searchNode(e.target.value));
  document.getElementById("center-btn")?.addEventListener("click", () => centerTree());
});
