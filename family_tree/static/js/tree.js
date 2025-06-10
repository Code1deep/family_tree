// static/js/tree.js
import { renderFamilyTree } from "./tree/core.js";

document.addEventListener('DOMContentLoaded', async () => {
  console.log("📦 DOMContentLoaded → Initialisation");

  const container = document.getElementById("wrapper");
  if (!container) {
    console.error("❌ Échec : élément #wrapper introuvable");
    return;
  }

  try {
    const res = await fetch("/api/tree/tree-data");
    if (!res.ok) throw new Error("Données arbre introuvables");
    const data = await res.json();
    await renderFamilyTree("wrapper", data);
  } catch (err) {
    alert("Erreur lors du chargement de l’arbre généalogique.");
    console.error(err);
  }
});
