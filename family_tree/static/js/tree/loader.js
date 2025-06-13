// static/js/tree/loader.js
import { loadTreeData, transformDataForD3, initMainD3Tree } from '/static/js/tree/core.js';

document.addEventListener("DOMContentLoaded", async () => {
    const treeContainer = document.getElementById("wrapper");
    if (!treeContainer) return;

    try {
        const rootId = 1; // Peut être dynamique via dataset/template
        const rawData = await loadTreeData(rootId);
        const d3Data = transformDataForD3(rawData);
        initMainD3Tree("wrapper", d3Data);
    } catch (error) {
        console.error("❌ Erreur d'initialisation de l’arbre :", error);
        treeContainer.innerHTML = `<div class="alert alert-danger">Erreur de chargement de l'arbre.</div>`;
    }
});
