// static/js/tree/d3-tree.js
import { downloadURL, toggleFullscreen, centerTree } from '/static/js/tree/utils.js';
import { openModal } from '/static/js/modal.js';

// Définition des couleurs pour chaque génération (0 à 9)
const generationColors = [
  "#F1C40F", // Jaune clair
  "#E67E22", // Orange clair
  "#1ABC9C", // Turquoise clair
  "#F39C12", // Orange doux
  "#2ECC71", // Vert clair
  "#c9f8fc", // Bleu clair
  "#fabebe", // Violet clair
  "#f76c59", // Rouge vif mais lumineux
  "#d3fcbd", // Gris clair
  "#b9c26b"  // Bleu pastel
];

const textColors = [
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
];

/** CSS intégré dynamiquement */
const style = document.createElement("style");
style.innerHTML = `
.node circle {
    stroke: steelblue;
    stroke-width: 2px;
}
.node text {
    font: 14px sans-serif;
    pointer-events: none;
}
.node--highlight circle {
    fill: orange;
}
.link {
    fill: none;
    stroke: #ccc;
    stroke-width: 2px;
}
.node text.details { fill:rgb(56, 22, 248); text-decoration: underline; cursor: pointer; font: 11px sans-serif; }
    body {
    background-color:rgb(245, 239, 187); /* Gris très clair */
}
#rootSelector {
  padding: 4px;
  font-size: 14px;
}

`;
document.head.appendChild(style);

function showPersonDetails(d) {
    const p = d.data || {};
    const photo = p.photo || "/static/img/default.png";
    const bio = p.bio || "Aucune biographie disponible";
    const mother = p.mother || "Inconnue";
    const father = p.father || "Inconnu";

    const html = `
        <img src="${photo}" alt="Photo de ${p.name}">
        <h2>${p.name}</h2>
        <p><strong>Biographie :</strong> ${bio}</p>
        <p><strong>Parents :</strong> ${mother} & ${father}</p>
    `;
    openModal(html);
}

export function initSubD3Tree(containerId, data) {
  if (!document.getElementById("subtree-style")) {
    d3.select("head").append("style")
      .attr("id", "subtree-style")
      .html(`svg { display: block; overflow: visible; }
      .link { fill: none; stroke: #ccc; stroke-width: 1.5px; }
      .node circle { stroke: #555; stroke-width: 1.5px; cursor: pointer; fill: #fff; transition: fill 0.2s; }
      .node circle:hover { fill: #f0f0f0; }
      .node text { font: 12px sans-serif; }

      .node--highlight circle { fill: orange !important; }`);
  }

  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = '';

  const CONFIG = {
    MARGIN: { top: 50, right: 120, bottom: 50, left: 120 },
    GENERATION_HEIGHT: 160,
    SIBLING_SPACING: 30,
    CLUSTER_CELL_WIDTH: 40,
    CLUSTER_CELL_HEIGHT: 30,
    CLUSTER_COLUMNS: 10
  };

  const root = d3.hierarchy(data);
  const width = Math.max(container.clientWidth, 1200);

  const generationMap = new Map();

  const maxDepth = root.height;
  const maxSiblings = d3.max(root.descendants(), d => d.parent ? d.parent.children.length : 1);

  const containerWidth = Math.max(container.clientWidth, 1200);
  const containerHeight = Math.max(container.clientHeight, 800);

  const GENERATION_HEIGHT = Math.max(containerHeight / (maxDepth + 1), 120);
  const SIBLING_SPACING = Math.max(containerWidth / (maxSiblings + 1), 40);

  const CLUSTER_COLUMNS = Math.ceil(Math.sqrt(maxSiblings));
  const CLUSTER_CELL_WIDTH = Math.max(containerWidth / CLUSTER_COLUMNS / 1.5, 40);
  const CLUSTER_CELL_HEIGHT = 40;

  console.log(`📏 AUTO-LAYOUT:
    ➜ maxDepth: ${maxDepth}
    ➜ maxSiblings: ${maxSiblings}
    ➜ GENERATION_HEIGHT: ${GENERATION_HEIGHT}
    ➜ SIBLING_SPACING: ${SIBLING_SPACING}
    ➜ CLUSTER_COLUMNS: ${CLUSTER_COLUMNS}
    ➜ CLUSTER_CELL_WIDTH: ${CLUSTER_CELL_WIDTH}`);

  root.eachBefore(node => {
    const genId = `${node.data.generation}_${node.data.period}_${node.data.parents_id || 'root'}`;
    if (!generationMap.has(genId)) {
      generationMap.set(genId, generationMap.size);
    }
    node.generationIndex = generationMap.get(genId);
    console.log(`[GENERATION] ${node.data.name} => GenIndex: ${node.generationIndex}`);
  });

  root.eachBefore(node => {
    node.x = node.generationIndex * CONFIG.GENERATION_HEIGHT;

    if (node.parent) {
      const siblings = node.parent.children;
      const siblingCount = siblings.length;
      const index = siblings.indexOf(node);

      if (siblingCount > 50) {
        const col = index % CONFIG.CLUSTER_COLUMNS;
        const row = Math.floor(index / CONFIG.CLUSTER_COLUMNS);

        // ✅ Patch : largeur/hauteur minimum
        const cellWidth = Math.max(CONFIG.CLUSTER_CELL_WIDTH, 80);
        const cellHeight = Math.max(CONFIG.CLUSTER_CELL_HEIGHT, 60);

        node.y = (col * cellWidth)
                - ((Math.min(siblingCount, CONFIG.CLUSTER_COLUMNS) * cellWidth) / 2)
                + (width / 2);

        node.x += row * cellHeight;

        console.log(`[GRID] ${node.data.name} | index: ${index} | col: ${col} | row: ${row} | y: ${node.y} | x: ${node.x}`);
      } else {
        const minSpacing = 60;
        const spacing = Math.max(CONFIG.SIBLING_SPACING, minSpacing);

        node.y = (index * spacing)
                - ((siblingCount - 1) * spacing) / 2
                + (width / 2);
      }
    } else {
      node.y = width / 2;
    }

    console.log(`📍 NODE "${node.data.name}": x=${node.x.toFixed(2)}, y=${node.y.toFixed(2)}`);
  });

  const height = d3.max(root.descendants(), d => d.x) + CONFIG.GENERATION_HEIGHT;
  const totalWidth = width + CONFIG.MARGIN.left + CONFIG.MARGIN.right;

  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", totalWidth)
    .attr("height", height + CONFIG.MARGIN.top + CONFIG.MARGIN.bottom)
    .attr("viewBox", [0, 0, totalWidth, height + CONFIG.MARGIN.top + CONFIG.MARGIN.bottom]);

  const gZoom = svg.append("g")
    .attr("transform", `translate(${CONFIG.MARGIN.left},${CONFIG.MARGIN.top})`);
  const g = gZoom.append("g");

  svg.call(d3.zoom()
    .scaleExtent([0.1, 3])
    .on("zoom", (e) => g.attr("transform", e.transform)));

  const node = g.selectAll(".node")
    .data(root.descendants())
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", d => {
      const transform = `translate(${d.y},${d.x})`;
      console.log(`🔄 TRANSFORM "${d.data.name}": ${transform}`);
      return transform;
    });

  node.append("circle")
    .attr("r", 20)
    .style("cursor", "pointer")
    .attr("fill", d => {
        const colorIndex = d.depth % generationColors.length;
        const color = generationColors[colorIndex];
        console.log(`🎨 Nœud ${d.data.name} - Profondeur ${d.depth} → Couleur ${color} (index ${colorIndex})`);
        return color;
    })
    .attr("stroke", "#333") // contour discret
    .attr("stroke-width", 5)
    .each(function(d) {
      const bbox = this.getBBox();
      console.log(`⚪️ BBox Circle "${d.data.name}": x=${bbox.x}, y=${bbox.y}, w=${bbox.width}, h=${bbox.height}`);
    });

  node.append("text")
    .attr("x", d => d.children ? -12 : 12)
    .attr("dy", 3)
    .style("text-anchor", d => d.children ? "end" : "start")
    .style("fill", d => {
      const colorIndex = d.depth % textColors.length;
      return textColors[colorIndex];
    })
    .style("opacity", 0)
    .text(d => d.data.name)
    .transition()
    .duration(800)
    .style("opacity", 1)
    .on("end", function(d) {
      const bbox = this.getBBox();
      console.log(`🔤 BBox Text "${d.data.name}": x=${bbox.x}, y=${bbox.y}, w=${bbox.width}, h=${bbox.height}`);
      if (bbox.width + 20 > CONFIG.SIBLING_SPACING) {
        console.warn(`⚠️ SPACING trop petit pour "${d.data.name}"`);
      }
    });

  g.selectAll(".link")
    .data(root.links())
    .enter().append("path")
    .attr("class", "link")
    .attr("d", d => {
      const path = d3.linkVertical().x(d => d.y).y(d => d.x)(d);
      console.log(`🔗 LINK "${d.source.data.name}" ➜ "${d.target.data.name}"`);
      return path;
    });

  node.append("text")
    .attr("class", "details")
    .attr("dy", "1.5em")
    .attr("x", 0)
    .text("👁 Voir les détails")
    .on("click", (event, d) => {
      console.log(`👁 Détails cliqués : ${d.data.name}`);
    });

  const drag = d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);

  // ✅ Dé-commenter pour activer le drag
  // node.call(drag);

  function dragstarted(event, d) {
    d3.select(this).raise().attr("stroke", "black");
  }

  function dragged(event, d) {
    d3.select(this).attr("transform", `translate(${event.x},${event.y})`);
  }

  function dragended(event, d) {
    d3.select(this).attr("stroke", null);
  }
}

// === Aller à génération X === 
export function setupGenerationJump(root, g, zoom) {
  console.log("✅ setupGenerationJump appelé 05 Juillet2025");
  const select = document.getElementById("goto-generation");
  const jumpBtn = document.getElementById("genBtn");

  select.innerHTML = "";
  const maxGen = d3.max(root.descendants(), d => d.depth);
  console.log("root.descendants() 05 juillet2025:", root.descendants());
  console.log("maxGen :", maxGen);

  for (let i = 0; i <= root.height; i++) {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = `Génération ${i}`;
    select.appendChild(opt);
  } 

  jumpBtn.onclick = () => {
    const gen = parseInt(select.value);
    console.log("➡️ Aller à génération :", gen);
    const target = root.descendants().find(d => d.depth === gen);

    if (target) {
      console.log(`🎯 Premier nœud génération ${gen} → ${target.data.name} (ID:${target.data.id})`);

      // === Recalcule offset EXACT ===
      const width = 1600;
      const height = 1000;
      const minX = d3.min(root.descendants(), d => d.x);
      const maxX = d3.max(root.descendants(), d => d.x);
      const xOffset = (width - (maxX - minX)) / 2 - minX;

      const cx = target.x + xOffset; // position horizontale centrée
      const cy = target.y;           // position verticale

      console.log(`📌 Marqueur sur x: ${cx}, y: ${cy}`);

      // ✅ Zoom :
      const transform = d3.zoomIdentity
        .translate(200, 200)
        .translate(-cx, -cy);

      d3.select(g.node().parentNode)
        .transition().duration(750)
        .call(zoom.transform, transform);

      // === Supprimer précédent ===
      d3.select(g.node().parentNode).selectAll(".gen-highlight").remove();

      // === Cercle clignotant positionné correctement ===
      g.append("circle")
        .attr("class", "gen-highlight")
        .attr("cx", cx)
        .attr("cy", cy - 30) // au-dessus du nœud
        .attr("r", 10)
        .style("fill", "red")
        .style("opacity", 0.8)
        .transition()
        .duration(500)
        .style("opacity", 0.1)
        .transition()
        .duration(500)
        .style("opacity", 0.8)
        .on("end", function repeat() {
          d3.select(this)
            .transition().duration(500).style("opacity", 0.1)
            .transition().duration(500).style("opacity", 0.8)
            .on("end", repeat);
        });

    } else {
      alert("❌ Aucun noeud pour cette génération !");
    }
  };
}

function setupTreeSearch(root, g) {
    console.log("✅ setupTreeSearch appelé 28 juin2025");
  const input = document.getElementById('treeSearch');
  if (!input) return;

  // ✅ Nettoyer avant :
  input.oninput = null;

  input.oninput = debounce(() => {
    const query = input.value.trim().toLowerCase();
    console.log("🔍 Recherche :", query);

    g.selectAll('.node')
      .classed('node--highlight', d => d.data.name.toLowerCase().includes(query));
  }, 300);
}

function setupResizeHandler(redrawFn) {
    window.addEventListener("resize", debounce(() => redrawFn(), 300));
}

export function setupCenterButton(containerId, g, svg, zoom, baseTranslate) {
  const centerBtn = document.getElementById('centerBtn');
  if (!centerBtn) {
    console.error("❌ ERREUR CRITIQUE : Bouton #centerBtn introuvable");
    return;
  }

  centerBtn.onclick = null;

  centerBtn.addEventListener('click', () => {
    console.log("🔄 Tentative de centrage...");
    try {
      const container = document.getElementById(containerId);
      if (!container) throw new Error("Conteneur introuvable");
      if (!g?.node()) throw new Error("Groupe SVG invalide");
      if (!zoom) throw new Error("Zoom non initialisé");

      console.log("✅ Éléments valides, appel à centerTree");
      centerTree(g, container, zoom, baseTranslate); // ✅
    } catch (err) {
      console.error("❌ Échec du centrage :", err.message);
    }
  });
}

function setupExportButtons(containerId) {
    const exportSvgBtn = document.getElementById("svgBtn");
    const exportPngBtn = document.getElementById("pngBtn");

    if (exportSvgBtn) {
        exportSvgBtn.addEventListener("click", () => exportAsSVG(containerId));
    }
    if (exportPngBtn) {
        exportPngBtn.addEventListener("click", () => exportAsPNG(containerId));
    }
}

function exportAsSVG(containerId) {
    const svg = document.querySelector(`#${containerId} svg`);
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadURL(url, "genealogy-tree.svg");
}

function exportAsPNG(containerId) {
    const svgNode = document.querySelector(`#${containerId} svg`);
    if (!svgNode) {
        console.error("❌ SVG introuvable pour export PNG");
        return;
    }

    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgNode);

    // On remplace getBBox() par getBoundingClientRect()
    const rect = svgNode.getBoundingClientRect();
    const width = rect.width || 1200;
    const height = rect.height || 800;

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");

    const img = new Image();
    const svgBlob = new Blob([svgString], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);

    img.onload = function () {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);

        const imgURI = canvas.toDataURL("image/png").replace("image/png", "octet/stream");
        downloadURL(imgURI, "genealogy-tree.png");
    };

    img.onerror = function (e) {
        console.error("❌ Erreur chargement image PNG", e);
        URL.revokeObjectURL(url);
    };

    img.src = url;
}

export function transformDataForD3(rawData) {
    return d3.hierarchy(rawData);
}

// Les fonctions suivantes sont conservées si besoin futur, mais non utilisées dans ce fichier.
/*
function update(source) {}
function zoomed(event) {}
*/

/* Fonction inutilisée mais conservée si besoin futur */
function update(source) {
    // Logique de mise à jour optimisée (non utilisée ici)
}

function zoomed(event) {
    // Inutilisé également, géré directement dans initD3Tree
}
