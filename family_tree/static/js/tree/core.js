// static/js/tree/core.js
import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { transformDataForD3 } from './d3-tree.js';
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import { centerTree, exportTreeAsPNG, exportTreeAsSVG, toggleFullscreen } from './utils.js';

let currentScale = 1;
let svgRoot;
let zoomBehavior;

export const initMainTree = () => {
    console.log("🌳 Initialisation arbre principal D3");
    const tryInit = async () => {
    const container = document.querySelector("main") || document.body;

    console.log("✅ tree-container trouvé");
    try {
      const res = await fetch("/api/tree/tree-data");
      if (!res.ok) throw new Error("Erreur lors du chargement des données arbre");
      const data = await res.json();
      initMainD3Tree("tree-container", data);
    } catch (err) {
      console.error("❌ Erreur de chargement de l'arbre :", err);
    }
};

  tryInit();
};

export function searchNode(query) {
    const searchTerm = query.toLowerCase();
    if (!svgRoot) return;
    svgRoot.selectAll("g.node text")
    .style("fill", d => d.data.name.toLowerCase().includes(searchTerm) ? "red" : "black")
    .style("font-weight", d => d.data.name.toLowerCase().includes(searchTerm) ? "bold" : "normal");
}

export async function initMainD3Tree(containerId, data) {
    const margin = { top: 50, right: 200, bottom: 50, left: 200 };
    const width = 2000 - margin.left - margin.right;
    const height = 1200 - margin.top - margin.bottom;

    const container = d3.select("main").empty() ? d3.select("body") : d3.select("main");
    container.selectAll("*").remove(); // Nettoyer avant de dessiner l’arbre


  if (!document.getElementById("tree-style")) {
    d3.select("head").append("style")
      .attr("id", "tree-style")
      .html(`
        .node circle { fill: #999; stroke: #555; stroke-width: 1.5px; }
        .node text { font: 10px sans-serif; }
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

    svgRoot = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

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
        d.children = newData.children.map(transformDataForD3).map(c => d3.hierarchy(c));
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
      .on("mouseover", function(event, d) {
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

  d3.select("#centerBtn").on("click", () => {
    const svgNode = container.select("svg").node();
    centerTree(svgRoot, svgNode.parentElement);
  });

  d3.select("#pngBtn").on("click", () => {
    exportTreeAsPNG(container.select("svg").node());
  });

  d3.select("#svgBtn").on("click", () => {
    exportTreeAsSVG(container.select("svg").node());
  });

  d3.select("#fullscreenBtn").on("click", () => {
    toggleFullscreen(container.node());
  });

  d3.select("#treeSearch").on("input", function () {
    searchNode(this.value);
  });

  update(root);

  setTimeout(() => {
    const svgNode = container.select("svg").node();
    centerTree(svgRoot, svgNode.parentElement);
  }, 700);
}

export function zoomIn() {
    currentScale = Math.min(currentScale * 1.2, 4);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.05);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function exportPNG(container) {
    const svgNode = container.querySelector('svg');
    const svgData = new XMLSerializer().serializeToString(svgNode);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    canvas.width = svgNode.clientWidth * 2;
    canvas.height = svgNode.clientHeight * 2;
    ctx.scale(2, 2);

    img.onload = () => {
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        const pngUrl = canvas.toDataURL("image/png");
        const link = document.createElement("a");
        link.download = "tree.png";
        link.href = pngUrl;
        link.click();
    };
    img.src = url;
}

export function exportSVG(container) {
    const svg = container.querySelector("svg");
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.download = "tree.svg";
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
}

export async function loadTreeData(rootId) {
    const response = await fetch(`/api/person/api/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur lors du chargement des données");
    return await response.json();
}
