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

export function setupAdvancedSearch(root, svgRoot, zoom, width, height) {
  const searchInput2 = document.getElementById("treeSearch2");
  const searchBtn2 = document.getElementById("searchBtn2");
  const searchField2 = document.getElementById("searchField2");

  // Nouveau conteneur suggestions isolé
  const suggestionBox2 = document.createElement("ul");
  suggestionBox2.style.position = "absolute";
  suggestionBox2.style.background = "white";
  suggestionBox2.style.border = "1px solid #ccc";
  suggestionBox2.style.listStyle = "none";
  suggestionBox2.style.padding = "0";
  suggestionBox2.style.margin = "0";
  suggestionBox2.style.width = searchInput2.offsetWidth + "px";
  suggestionBox2.style.zIndex = "1000";
  suggestionBox2.style.maxHeight = "200px";
  suggestionBox2.style.overflowY = "auto";
  searchInput2.parentNode.style.position = "relative";
  searchInput2.parentNode.appendChild(suggestionBox2);

  searchInput2.addEventListener("keyup", (e) => {
    const term = e.target.value.toLowerCase().trim();
    const field = searchField2.value;
    suggestionBox2.innerHTML = "";

    if (term.length === 0) return;

    const matches = root.descendants().filter(d => {
      const val = field === "name"
        ? d.data.name?.toLowerCase()
        : field === "birth_year"
          ? String(d.data.birth_year || "")
          : String(d.depth);

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
        focusNode2(match);
        suggestionBox2.innerHTML = "";
      });

      suggestionBox2.appendChild(li);
    });
  });

  searchBtn2.addEventListener("click", () => {
    const term = searchInput2.value.toLowerCase().trim();
    const field = searchField2.value;

    const match = root.descendants().find(d => {
      const val = field === "name"
        ? d.data.name?.toLowerCase()
        : field === "birth_year"
          ? String(d.data.birth_year || "")
          : String(d.depth);

      return val.includes(term);
    });

    if (match) {
      focusNode2(match);
    } else {
      alert("Aucun résultat !");
    }

    suggestionBox2.innerHTML = "";
  });

  function focusNode2(node) {
    if (node._children) {
      node.children = node._children;
      node._children = null;
    }
    // Relance ton update
    update(node);

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

