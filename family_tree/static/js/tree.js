// static/js/tree.js
import { loadTreeData } from './tree/core.js';
import { initD3Tree } from './tree/d3-tree.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const treeData = await loadTreeData(1); // Charge les données JSON
        initD3Tree(treeData); // Affiche avec D3
    } catch (error) {
        console.error("Erreur:", error);
        alert("Erreur de chargement de l'arbre");
    }
});

