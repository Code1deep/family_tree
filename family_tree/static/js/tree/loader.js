//static/js/tree/loader.js 
import { loadTreeData, transformDataForD3 } from './tree/core.js';
import { initD3Tree } from './d3-tree.js';

document.addEventListener("DOMContentLoaded", async () => {
    const treeContainer = document.getElementById("tree-container");
    if (!treeContainer) return;

    try {
        const rootId = 1; // Ou récupérer depuis le template
        const rawData = await loadTreeData(rootId);
        const d3Data = transformDataForD3(rawData);
        initD3Tree("tree-container", d3Data);
    } catch (error) {
        console.error("Failed to initialize tree:", error);
        treeContainer.innerHTML = `<div class="alert alert-danger">Erreur de chargement de l'arbre</div>`;
    }
});
