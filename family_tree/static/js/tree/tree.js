// static/js/tree/tree.js
// ✅ Importation des modules
import { renderFamilyTree } from '/static/js/tree/core.js';
import {
  toggleFullscreen,
  exportAsPNG,
  exportSVG,
  centerTree,
  searchNode
} from '/static/js/tree/utils.js';
import { openModal } from '/static/js/modal.js';
import { initMainD3Tree, initSubD3Tree } from '/static/js/tree/index.js';
import { setupCenterButton } from '/static/js/tree/d3-tree.js';

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
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const searchField = document.getElementById("searchField");
  
  // 🟢 Si tu veux une boîte de suggestions
  const suggestionBox = document.createElement("ul");
  suggestionBox.style.position = "absolute";
  suggestionBox.style.background = "white";
  suggestionBox.style.border = "1px solid #ccc";
  suggestionBox.style.listStyle = "none";
  suggestionBox.style.padding = "0";
  suggestionBox.style.margin = "0";
  suggestionBox.style.width = searchInput.offsetWidth + "px";
  suggestionBox.style.zIndex = "1000";
  suggestionBox.style.maxHeight = "200px";
  suggestionBox.style.overflowY = "auto";
  
  searchInput.parentNode.style.position = "relative";
  searchInput.parentNode.appendChild(suggestionBox);
  
  // 🔎 Suggestions dynamiques
  searchInput.addEventListener("keyup", (e) => {
    const term = e.target.value.toLowerCase().trim();
    const field = searchField.value;
    suggestionBox.innerHTML = "";
  
    if (term.length === 0) return;
  
    const matches = root.descendants().filter(d => {
      let val = "";
      if (field === "name") val = d.data.name?.toLowerCase();
      else if (field === "birth_year") val = String(d.data.birth_year || "");
      else if (field === "generation") val = String(d.depth);
  
      return val.includes(term);
    }).slice(0, 10);
  
    matches.forEach(match => {
      const li = document.createElement("li");
      li.textContent = field === "name"
        ? match.data.name
        : field === "birth_year"
          ? `${match.data.name} (${match.data.birth_year || "?"})`
          : `${match.data.name} (Gen ${match.depth})`;
  
      li.style.cursor = "pointer";
      li.style.padding = "4px 8px";
      li.style.borderBottom = "1px solid #eee";
  
      li.addEventListener("click", () => {
        focusNode(match);
        suggestionBox.innerHTML = "";
      });
  
      suggestionBox.appendChild(li);
    });
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

