// static/js/tree.js
// tree.js
function drawTree(data) {
  const nodes = data.nodes;
  const edges = data.edges;

  // Préparer les données sous forme de hiérarchie
  const nodeById = new Map(nodes.map(d => [d.id, { ...d, children: [] }]));
  edges.forEach(edge => {
    const parent = nodeById.get(edge.from);
    const child = nodeById.get(edge.to);
    if (parent && child) parent.children.push(child);
  });

  // Trouver la racine (nœud sans parent)
  const allChildIds = new Set(edges.map(e => e.to));
  const root = nodes.find(n => !allChildIds.has(n.id));
  if (!root) {
    console.error("❌ Impossible de déterminer la racine");
    return;
  }

  const hierarchyRoot = d3.hierarchy(nodeById.get(root.id));

  // Définir dimensions et marges
  const width = document.getElementById("wrapper").clientWidth;
  const height = document.getElementById("wrapper").clientHeight;
  const margin = { top: 20, right: 90, bottom: 30, left: 90 };

  // Nettoyer le conteneur
  d3.select("#wrapper").selectAll("*").remove();

  const svg = d3.select("#wrapper")
    .append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("preserveAspectRatio", "xMidYMid meet");

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Appliquer layout tree
  const treeLayout = d3.tree().size([width - 2 * margin.left, height - 2 * margin.top]);
  treeLayout(hierarchyRoot);

  // Liens
  g.selectAll(".link")
    .data(hierarchyRoot.links())
    .join("path")
    .attr("class", "link")
    .attr("fill", "none")
    .attr("stroke", "#ccc")
    .attr("stroke-width", 2)
    .attr("d", d3.linkVertical()
      .x(d => d.x)
      .y(d => d.y)
    );

  // Nœuds
  const node = g.selectAll(".node")
    .data(hierarchyRoot.descendants())
    .join("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${d.x},${d.y})`);

  node.append("circle")
    .attr("r", 20)
    .attr("fill", "#1e90ff")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2);

  node.append("text")
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .attr("fill", "#fff")
    .text(d => d.data.name);
}

async function loadAndDrawTree() {
  try {
    const response = await fetch("/api/tree/tree-data");
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    const data = await response.json();
    console.log("✅ Données arbre chargées :", data);
    drawTree(data);
  } catch (err) {
    console.error("❌ Erreur lors du chargement des données :", err);
    const wrapper = document.getElementById("wrapper");
    wrapper.innerHTML = `<div style="color: red;">Erreur chargement arbre: ${err.message}</div>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadAndDrawTree();
});
