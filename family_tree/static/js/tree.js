// static/js/tree.js
import { loadTreeData } from './tree/core.js';
import { zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js'; 
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';

// Initialisation directe si les données sont déjà disponibles
initSubD3Tree("modal-tree-container", miniTreeData);

// Facultatif : exposer pour debug
window.initD3Tree = initMainD3Tree;

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
