// static/js/tree/tree.js
// ✅ Importation des modules
import { renderFamilyTree } from './core.js';
import {
  toggleFullscreen,
  exportAsPNG,
  exportSVG,
  centerTree,
  searchNode
} from './utils.js';
import { openModal } from '../modal.js';
import { initMainD3Tree, initSubD3Tree } from './index.js';
import { setupCenterButton } from './d3-tree.js';

console.log("✅ tree.js chargé depuis :", import.meta.url);
window.initD3Tree = initMainD3Tree;

/* ✅ Conversion utile au besoin — non utilisée si l'API est prête */
function convertToHierarchy(data) {
  console.log("🔄 Conversion {nodes, edges} → hiérarchie");
  const nodeById = {};
  data.nodes.forEach(n => {
    nodeById[n.id] = { ...n, children: [] };
  });
  data.edges.forEach(e => {
    const parent = nodeById[e.from];
    const child = nodeById[e.to];
    if (parent && child) parent.children.push(child);
  });

  const allChildIds = new Set(data.edges.map(e => e.to));
  const root = data.nodes.find(n => !allChildIds.has(n.id));
  if (!root) {
    console.error("❌ Racine introuvable");
    return null;
  }

  console.log("✅ Racine trouvée :", root);
  console.log("🌳 root défini :", root);
  console.log("🌳 root.descendants :", root.descendants());

  return nodeById[root.id];
}

window.skipAutoInit = true;

/* ✅ DOMContentLoaded = point d'entrée unique */
document.addEventListener("DOMContentLoaded", async () => {
  console.log("📦 DOMContentLoaded → Initialisation");

  const treeContainer = document.getElementById("wrapper");
  if (!treeContainer) {
    console.error("❌ Échec : élément #wrapper introuvable");
    return;
  }

  try {
    console.log("📡 Fetch vers /api/tree/ ...");
    const response = await fetch("/api/tree/");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const treeData = await response.json();
    console.log("✅ Données reçues :", treeData);

    console.log("🌳 Appel à renderFamilyTree ...");
    const { g, svgRoot, zoom, baseTranslate } = await renderFamilyTree("wrapper", treeData);

    console.log("✅ Arbre affiché avec succès");

    /* ⚡ setupCenterButton reçoit les bons paramètres */
    setupCenterButton("wrapper", g, svgRoot, zoom, baseTranslate);

  } catch (err) {
    console.error("❌ Erreur chargement arbre :", err);
  }

  /* ✅ Boutons UI directs */
  document.getElementById("fullscreenBtn")?.addEventListener("click", () => {
    console.log("🖥️ Clic : Plein écran");
    toggleFullscreen(treeContainer);
  });

  document.getElementById("pngBtn")?.addEventListener("click", () => {
    console.log("📷 Clic : Export PNG");
    exportAsPNG("wrapper");
  });

  document.getElementById("svgBtn")?.addEventListener("click", () => {
    console.log("📐 Clic : Export SVG");
    exportSVG(document.querySelector("#wrapper svg"));
  });
});

export function setupAdvancedSearch(root, svgRoot, zoom, width, height, update) {
  console.log("✅ JS de recherche chargé");
  
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const searchField = document.getElementById("searchField");
  
  console.log("searchInput =", searchInput);
  console.log("searchBtn =", searchBtn);
  console.log("searchField =", searchField);
  
  searchBtn.addEventListener("click", () => {
    console.log("✅ Bouton recherche cliqué !");
    const term = searchInput.value.toLowerCase().trim();
    const field = searchField.value;
  
    console.log("Terme =", term, "Field =", field);
  
    const match = root.descendants().find(d => {
      let val = "";
      if (field === "name") val = d.data.name?.toLowerCase();
      else if (field === "birth_year") val = String(d.data.birth_year || "");
      else if (field === "generation") val = String(d.depth);
  
      return val.includes(term);
    });
  
    console.log("Match trouvé :", match);
  
    if (match) {
      focusNode(match);
    } else {
      alert("Aucun résultat !");
    }
  });
  
  // 🔍 Clic bouton
  searchBtn.addEventListener("click", () => {
    const term = searchInput.value.toLowerCase().trim();
    const field = searchField.value;
  
    const match = root.descendants().find(d => {
      let val = "";
      if (field === "name") val = d.data.name?.toLowerCase();
      else if (field === "birth_year") val = String(d.data.birth_year || "");
      else if (field === "generation") val = String(d.depth);
  
      return val.includes(term);
    });
  
    if (match) {
      focusNode(match);
    } else {
      alert("Aucun résultat !");
    }
  
    suggestionBox.innerHTML = "";
  });
  
  // 📌 Ta fonction de centrage (tu l’as sûrement déjà)
  function focusNode(node) {
    if (node._children) {
      node.children = node._children;
      node._children = null;
      update(node);
    }
  
    const x = node.x;
    const y = node.y;
  
    svgRoot.transition().duration(750).call(
      zoom.transform,
      d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1)
        .translate(-y, -x)
    );
  }

}

