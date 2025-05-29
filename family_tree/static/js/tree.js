// static/js/tree.js
<script src="https://balkan.app/js/OrgChart.js"></script>

import { loadTreeData } from './tree/core.js';
import { renderFamilyTree } from './tree/d3-tree.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const treeData = await loadTreeData(1); // Charge les données
        renderFamilyTree(treeData); // Affiche l'arbre
    } catch (error) {
        console.error("Erreur:", error);
        alert("Erreur de chargement de l'arbre");
    }
});
