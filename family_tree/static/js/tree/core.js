// static/js/tree/core.js
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

// 👇 À exporter uniquement, pas d'exécution immédiate
export async function renderFamilyTree(containerId, data) {
  console.log("🧬 Démarrage de renderFamilyTree()", data);

  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`❌ Conteneur introuvable : #${containerId}`);
    return;
  }

  // 🧹 Nettoyage de l’arbre précédent s’il existe
  container.innerHTML = "";

  // 📏 Dimensions
  const width = container.clientWidth;
  const height = container.clientHeight;
  const margin = { top: 20, right: 90, bottom: 30, left: 90 };

  const svg = d3.select(container)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 👨‍👩‍👧‍👦 Construction des nœuds et liens
  const stratify = d3.stratify()
    .id(d => d.id)
    .parentId(d => d.parent_id);

  const root = stratify(data.nodes);
  const treeLayout = d3.tree().size([height, width - 200]);
  treeLayout(root);

  // 🔗 Liens
  svg.selectAll(".link")
    .data(root.links())
    .enter().append("path")
    .attr("class", "link")
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x));

  // 🔘 Nœuds
  const node = svg.selectAll(".node")
    .data(root.descendants())
    .enter().append("g")
    .attr("class", d => "node ft-node ft-gener-" + (d.depth || 0))
    .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
    .attr("r", 6);

  node.append("text")
    .attr("dy", 3)
    .attr("x", d => d.children ? -12 : 12)
    .style("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name);

  console.log("✅ Arbre dessiné dans #", containerId);
}
