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
  const input = document.getElementById("treeSearch2");
  const btn = document.getElementById("searchBtn2");
  const field = document.getElementById("searchField2");

  // ✅ Boîte suggestions unique
  const box = document.createElement("ul");
  box.style.position = "absolute";
  box.style.background = "#fff";
  box.style.border = "1px solid #ccc";
  box.style.padding = "0";
  box.style.margin = "0";
  box.style.listStyle = "none";
  box.style.width = input.offsetWidth + "px";
  box.style.maxHeight = "200px";
  box.style.overflowY = "auto";
  box.style.zIndex = "9999";
  input.parentNode.style.position = "relative";
  input.parentNode.appendChild(box);

  input.addEventListener("keyup", (e) => {
    const val = input.value.trim().toLowerCase();
    const fieldVal = field.value;

    box.innerHTML = "";

    if (val.length < 1) return;

    const matches = root.descendants().filter(d => {
      if (fieldVal === "name") return d.data.name?.toLowerCase().includes(val);
      if (fieldVal === "birth_year") return String(d.data.birth_year || "").includes(val);
      if (fieldVal === "generation") return String(d.depth).includes(val);
      return false;
    }).slice(0, 10);

    matches.forEach(d => {
      const li = document.createElement("li");
      li.style.padding = "4px 8px";
      li.style.borderBottom = "1px solid #eee";
      li.style.cursor = "pointer";
      li.textContent = fieldVal === "name"
        ? d.data.name
        : fieldVal === "birth_year"
          ? `${d.data.name} (${d.data.birth_year || "?"})`
          : `${d.data.name} (Gen ${d.depth})`;
      li.onclick = () => {
        focusAndZoom(d);
        box.innerHTML = "";
      };
      box.appendChild(li);
    });
  });

  btn.addEventListener("click", () => {
    const val = input.value.trim().toLowerCase();
    const fieldVal = field.value;

    const match = root.descendants().find(d => {
      if (fieldVal === "name") return d.data.name?.toLowerCase().includes(val);
      if (fieldVal === "birth_year") return String(d.data.birth_year || "").includes(val);
      if (fieldVal === "generation") return String(d.depth).includes(val);
      return false;
    });

    if (match) {
      focusAndZoom(match);
      box.innerHTML = "";
    } else {
      alert("Aucun résultat !");
    }
  });

  function focusAndZoom(node) {
    if (node._children) {
      node.children = node._children;
      node._children = null;
    }
    update(node);

    svgRoot.transition().duration(750).call(
      zoom.transform,
      d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1)
        .translate(-node.y, -node.x)
    );
  }
}

