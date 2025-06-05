// static/js/tree/core.js
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import { centerTree, exportTreeAsPNG, exportTreeAsSVG, toggleFullscreen } from './utils.js';

let svgRoot, zoomBehavior, currentScale = 1;

export function initMainD3Tree(container, data) {
  console.log("🌳 initMainD3Tree appelé avec :", data);

  if (data.nodes && data.edges) {
    data = buildTreeFromGraph(data.nodes, data.edges);
    console.log("🌿 Arbre reconstruit :", data);
  }

  renderTree(data);
}

export function buildTreeFromGraph(nodes, edges) {
  const idNodeMap = {};
  const parentSet = new Set();

  nodes.forEach(n => {
    idNodeMap[n.id] = { ...n, children: [] };
  });

  edges.forEach(e => {
    const parent = idNodeMap[e.from];
    const child = idNodeMap[e.to];
    if (parent && child) {
      parent.children.push(child);
      parentSet.add(e.to);
    }
  });

  const rootNode = nodes.find(n => !parentSet.has(n.id));
  if (!rootNode) {
    console.error("❌ Aucune racine trouvée");
    return null;
  }

  return idNodeMap[rootNode.id];
}

export function renderTree(data) {
  const margin = { top: 50, right: 200, bottom: 50, left: 200 };
  const width = 2000 - margin.left - margin.right;
  const height = 1200 - margin.top - margin.bottom;

  const container = d3.select(".tree-wrapper").empty()
    ? d3.select("body").append("div").attr("class", "tree-wrapper")
    : d3.select(".tree-wrapper");

  container.selectAll("*").remove();

  if (!document.getElementById("tree-style")) {
    d3.select("head").append("style")
      .attr("id", "tree-style")
      .html(`
        .node circle { fill: #999; stroke: #555; stroke-width: 1.5px; }
        .node text { font: 12px sans-serif; }
        .link { fill: none; stroke: #ccc; stroke-width: 1.5px; }
        .tooltip {
          position: absolute; text-align: center; padding: 5px;
          font: 12px sans-serif; background: lightsteelblue;
          border: 1px solid #aaa; pointer-events: none; border-radius: 3px;
        }
        .tree-controls {
          margin: 10px 0; display: flex; gap: 10px;
        }
        .tree-controls input[type="text"],
        .tree-controls button {
          padding: 4px 10px; font-size: 14px;
        }
      `);
  }

  container.insert("div", ":first-child").attr("class", "tree-controls").html(`
    <input id="treeSearch" placeholder="Rechercher une personne..." />
    <button id="centerBtn">Centrer</button>
    <button id="pngBtn">Export PNG</button>
    <button id="svgBtn">Export SVG</button>
    <button id="fullscreenBtn">Plein écran</button>
  `);

  const svg = container.append("svg")
    .attr("viewBox", [0, 0, width + margin.left + margin.right, height + margin.top + margin.bottom])
    .style("width", "100%")
    .style("height", "90vh")
    .style("border", "1px solid #ccc");

  zoomBehavior = d3.zoom().scaleExtent([0.05, 4]).on("zoom", (event) => {
    svgRoot.attr("transform", event.transform);
    currentScale = event.transform.k;
  });

  svg.call(zoomBehavior);

  svgRoot = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const treeLayout = d3.tree().nodeSize([30, 300]);
  const root = d3.hierarchy(data, d => d.children || d._children);
  root.x0 = 0;
  root.y0 = 0;

  root.children?.forEach(collapse);

  const tooltip = container.append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  function collapse(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  }

  function diagonal(s, d) {
    return `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`;
  }

  async function onClick(event, d) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else if (d._children) {
      d.children = d._children;
      d._children = null;
    } else {
      try {
        const res = await fetch(`/api/person/visualize/tree/${d.data.id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const newData = await res.json();
        d.children = newData.children.map(c => d3.hierarchy(c));
      } catch (err) {
        console.error("❌ Erreur chargement enfants :", err);
      }
    }
    update(d);
  }

  function update(source) {
    const treeData = treeLayout(root);
    const nodes = treeData.descendants();
    const links = treeData.links();

    nodes.forEach(d => d.y = d.depth * 180);

    const node = svgRoot.selectAll("g.node")
      .data(nodes, d => d.data.id);

    const nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", d => `translate(${source.y0},${source.x0})`)
      .on("click", onClick)
      .on("mouseover", function (event, d) {
        tooltip.transition().duration(200).style("opacity", .9);
        tooltip.html(`<strong>${d.data.name}</strong><br>ID: ${d.data.id}`)
          .style("left", (event.pageX + 10) + "px")
          .style("top", (event.pageY - 20) + "px");
      })
      .on("mouseout", () => tooltip.transition().duration(300).style("opacity", 0));

    nodeEnter.append("circle")
      .attr("r", 1e-6)
      .style("fill", d => d._children ? "#555" : "#999");

    nodeEnter.append("text")
      .attr("dy", 3)
      .attr("x", d => d._children ? -10 : 10)
      .style("text-anchor", d => d._children ? "end" : "start")
      .text(d => d.data.name);

    const nodeUpdate = nodeEnter.merge(node);

    nodeUpdate.transition().duration(500)
      .attr("transform", d => `translate(${d.y},${d.x})`);

    nodeUpdate.select("circle")
      .attr("r", 4)
      .style("fill", d => d._children ? "#555" : "#999");

    node.exit().transition().duration(500)
      .attr("transform", d => `translate(${source.y},${source.x})`)
      .remove()
      .select("circle").attr("r", 0);

    const link = svgRoot.selectAll("path.link")
      .data(links, d => d.target.data.id);

    link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", d => diagonal(source, source))
      .merge(link)
      .transition().duration(500)
      .attr("d", d => diagonal(d.source, d.target));

    link.exit().transition().duration(500)
      .attr("d", d => diagonal(source, source))
      .remove();

    nodes.forEach(d => {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  // Fonctions utilitaires d’interaction
  function centerTree(svgGroup, wrapper) {
    const bounds = svgGroup.node().getBBox();
    const scale = Math.min(
      wrapper.clientWidth / bounds.width,
      wrapper.clientHeight / bounds.height,
      1
    );
    const translate = [
      (wrapper.clientWidth - bounds.width * scale) / 2 - bounds.x * scale,
      (wrapper.clientHeight - bounds.height * scale) / 2 - bounds.y * scale
    ];
    d3.select(svgGroup.node().ownerSVGElement)
      .transition().duration(750)
      .call(zoomBehavior.transform, d3.zoomIdentity.translate(...translate).scale(scale));
  }

  function exportTreeAsPNG(svgNode) {
    const svgData = new XMLSerializer().serializeToString(svgNode);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();
    const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      const png = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = png;
      a.download = "tree.png";
      a.click();
      URL.revokeObjectURL(url);
    };
    img.src = url;
  }

  function exportTreeAsSVG(svgNode) {
    const svgData = new XMLSerializer().serializeToString(svgNode);
    const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "tree.svg";
    a.click();
  }

  function toggleFullscreen(elem) {
    if (!document.fullscreenElement) {
      elem.requestFullscreen().catch(err => console.error(err));
    } else {
      document.exitFullscreen();
    }
  }

  function searchNode(query) {
    const term = query.trim().toLowerCase();
    svgRoot.selectAll("g.node text")
      .style("font-weight", d => d.data.name.toLowerCase().includes(term) ? "bold" : "normal")
      .style("fill", d => d.data.name.toLowerCase().includes(term) ? "red" : "black");
  }

  const svgNode = container.select("svg").node();
  if (!svgNode) {
    console.error("❌ Aucun SVG trouvé pour les actions");
} else {
  d3.select("#centerBtn").on("click", () => {
    centerTree(svgRoot, svgNode.parentElement);
  });

  d3.select("#pngBtn").on("click", () => {
    exportTreeAsPNG(svgNode);
  });

  d3.select("#svgBtn").on("click", () => {
    exportTreeAsSVG(svgRoot.node());
  });

  d3.select("#fullscreenBtn").on("click", () => {
    toggleFullscreen(container.node());
  });

  d3.select("#treeSearch").on("input", function () {
    searchNode(this.value);
  });

  update(root);

  setTimeout(() => {
    centerTree(svgRoot, svgNode.parentElement);
  }, 500);
}
}

export function zoomIn() {
    currentScale = Math.min(currentScale * 1.2, 4);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.05);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export async function loadTreeData(rootId) {
    const response = await fetch(`/api/person/api/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur lors du chargement des données");
    return await response.json();
}

export { exportTreeAsPNG as exportPNG, exportTreeAsSVG as exportSVG };
