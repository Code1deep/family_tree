// static/js/tree.js
import { loadTreeData } from './tree/core.js';
import { initD3Tree } from './tree/d3-tree.js';
import { zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js'; 
import { openModal } from "/static/js/modal.js";

window.initD3Tree = initD3Tree;

document.addEventListener("DOMContentLoaded", async () => {
  const treeContainer = document.getElementById("tree-container");
  if (!treeContainer) {
    console.error("❌ tree-container introuvable !");
    return;
  }

  try {
    const response = await fetch("/api/tree/");  // chemin correct et unique
    const treeData = await response.json();
    console.log("✅ Données reçues :", treeData);
    initD3Tree("#tree-container", treeData);
  } catch (err) {
    console.error("❌ Erreur lors du chargement de l’arbre :", err);
  }

  // Ajoute des vérifications de null pour éviter les erreurs :
  document.getElementById("center-btn")?.addEventListener("click", () => centerTree());
  document.getElementById("fullscreen-btn")?.addEventListener("click", () => toggleFullscreen(treeContainer));
  document.getElementById("export-png")?.addEventListener("click", () => exportPNG(treeContainer));
  document.getElementById("export-svg")?.addEventListener("click", () => exportSVG(treeContainer));
  document.getElementById("search-box")?.addEventListener("input", (e) => searchNode(e.target.value));
});
