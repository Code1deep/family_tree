// static/js/tree.js

// ✅ Chargement des modules
import { loadTreeData } from './tree/core.js';
import { zoomIn, zoomOut, exportPNG, exportSVG, searchNode } from './tree/core.js';
import { centerTree } from './tree/utils.js';
import { openModal } from "/static/js/modal.js";
import { initMainD3Tree, initSubD3Tree } from './tree/index.js';

// ✅ Confirmation de chargement
console.log('✅ tree.js loaded');

// ✅ Exposition facultative pour débogage
window.initD3Tree = initMainD3Tree;

document.addEventListener("DOMContentLoaded", async () => {
  // ✅ Cherche un conteneur générique (main ou body)
  const treeContainer =
    document.querySelector("main") ||
    document.querySelector(".tree-wrapper") ||
    document.body;

  if (!treeContainer) {
    console.error("❌ Aucun conteneur DOM valide trouvé pour afficher l’arbre !");
    return;
  }

  try {
    const response = await fetch("/api/tree/");
    if (!response.ok) throw new Error(`Erreur HTTP ${response.status}`);
    const treeData = await response.json();
    console.log("✅ Données reçues :", treeData);
    initMainD3Tree(treeContainer, treeData); // ⬅️ On passe l'élément, plus un ID
  } catch (err) {
    console.error("❌ Erreur lors du chargement de l’arbre :", err);
  }

  document.getElementById("fullscreen-btn")?.addEventListener("click", () => toggleFullscreen(treeContainer));
  document.getElementById("export-png")?.addEventListener("click", () => exportPNG(treeContainer));
  document.getElementById("export-svg")?.addEventListener("click", () => exportSVG(treeContainer));
  document.getElementById("search-box")?.addEventListener("input", (e) => searchNode(e.target.value));
  document.getElementById("center-btn")?.addEventListener("click", () => centerTree());
});
