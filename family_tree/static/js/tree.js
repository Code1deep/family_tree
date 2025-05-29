// static/js/tree.js
import { loadTreeData } from './tree/core.js';
import { initD3Tree } from './tree/d3-tree.js';

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
});
