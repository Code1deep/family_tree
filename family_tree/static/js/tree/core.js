// static/js/tree/core.js
console.log("✔ core.js initialisé");

console.log("🧠 core.js chargé");
const wrapper = document.getElementById("wrapper");
console.log("🔍 wrapper in core.js ?", wrapper);


import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { transformDataForD3 } from './d3-tree.js';
import {
  debounce,
  throttle,
  exportPNG,
  exportSVG,
  toggleFullscreen,
  buildTreeFromEdges,
  centerTree,
  searchNode
} from './utils.js';

let currentScale = 1;

// ===========================
// Fonction principale d’affichage D3.js (version hiérarchique)
export function initMainD3Tree(containerId, data) {
    const margin = { top: 50, right: 200, bottom: 50, left: 200 };
    const width = 2000 - margin.left - margin.right;
    const height = 1200 - margin.top - margin.bottom;

    const container = d3.select(`#${containerId}`);
    container.selectAll("*").remove(); // Clear previous tree

    if (!document.getElementById("tree-style")) {
        d3.select("head").append("style")
            .attr("id", "tree-style")
            .html(`
                .node circle { fill: #999; stroke: #555; stroke-width: 1.5px; }
                .node text { font: 10px sans-serif; }
                .link { fill: none; stroke: #ccc; stroke-width: 1.5px; }
                .tooltip { position: absolute; text-align: center; padding: 5px; font: 12px sans-serif; background: lightsteelblue; border: 1px solid #aaa; pointer-events: none; border-radius: 3px; }
                .tree-controls { margin: 10px 0; display: flex; gap: 10px; }
                .tree-controls input[type="text"] { padding: 2px 6px; font-size: 14px; }
                .tree-controls button { padding: 4px 10px; font-size: 14px; }
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
        .style("border", "1px solid #ccc")
        .call(d3.zoom().scaleExtent([0.05, 4]).on("zoom", zoomed))
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const treeLayout = d3.tree().nodeSize([30, 300]);

    const root = d3.hierarchy(data, d => d.children || d._children);
    root.x0 = 0;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    root.children?.forEach(collapse);
    update(root);

    const tooltip = container.append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("opacity", 0);

    function update(source) {
        const treeData = treeLayout(root);
        const nodes = treeData.descendants();
        const links = treeData.links();

        nodes.forEach(d => { d.y = d.depth * 180; });

        const node = svg.selectAll('g.node')
            .data(nodes, d => d.data.id);

        const nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", d => `translate(${source.y0},${source.x0})`)
            .on('click', onClick)
            .on('mouseover', function(event, d) {
                tooltip.transition().duration(200).style("opacity", .9);
                tooltip.html(`<strong>${d.data.name}</strong><br>ID: ${d.data.id}`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 20) + "px");
            })
            .on('mouseout', () => tooltip.transition().duration(300).style("opacity", 0));

        nodeEnter.append('circle')
            .attr('r', 1e-6)
            .style('fill', d => d._children ? "#555" : "#999");

        nodeEnter.append('text')
            .attr("dy", 3)
            .attr("x", d => d._children ? -10 : 10)
            .style("text-anchor", d => d._children ? "end" : "start")
            .text(d => d.data.name);

        const nodeUpdate = nodeEnter.merge(node);
        nodeUpdate.transition().duration(500).attr("transform", d => `translate(${d.y},${d.x})`);
        nodeUpdate.select('circle').attr('r', 4).style('fill', d => d._children ? "#555" : "#999");

        const nodeExit = node.exit().transition().duration(500)
            .attr("transform", d => `translate(${source.y},${source.x})`).remove();
        nodeExit.select('circle').attr('r', 0);
        nodeExit.select('text').style('fill-opacity', 0);

        const link = svg.selectAll('path.link')
            .data(links, d => d.target.data.id);
        const linkEnter = link.enter().insert('path', "g")
            .attr("class", "link")
            .attr('d', d => {
                const o = { x: source.x0, y: source.y0 };
                return diagonal(o, o);
            });
        linkEnter.merge(link).transition().duration(500).attr('d', d => diagonal(d.source, d.target));
        link.exit().transition().duration(500).attr('d', d => {
            const o = { x: source.x, y: source.y };
            return diagonal(o, o);
        }).remove();

        nodes.forEach(d => {
            d.x0 = d.x;
            d.y0 = d.y;
        });
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
                const response = await fetch(`/api/person/visualize/tree/${d.data.id}`);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const newData = await response.json();
                const newChildren = newData.children.map(transformDataForD3);
                d.children = newChildren.map(c => d3.hierarchy(c));
            } catch (error) {
                console.error("Erreur de chargement des enfants :", error);
            }
        }
        update(d);
    }

    function zoomed(event) {
        svg.attr("transform", event.transform);
    }

    // Controls
    d3.select("#centerBtn").on("click", () => {
        const svgNode = container.select("svg").node();
        centerTree(d3.select(svgNode).select("g"), svgNode.parentElement);
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
        const name = this.value.toLowerCase();
        svg.selectAll("g.node").select("text").each(function (d) {
            const match = d.data.name.toLowerCase().includes(name);
            d3.select(this).style("fill", match ? "red" : "#000");
        });
    });

    setTimeout(() => {
        const svgNode = container.select("svg").node();
        centerTree(d3.select(svgNode).select("g"), svgNode.parentElement);
    }, 700);
}

// ===========================
// Fonction d’affichage D3.js (version nodes+edges)
export async function drawTree(data) {
    console.log("✅ drawTree() started...");
    console.log("🟢 Données reçues pour dessiner l'arbre :", data);
    try {
        if (!data || !data.nodes || !data.edges) {
            console.error("❌ Données invalides pour drawTree:", data);
            console.error("❌ Données manquantes ou invalides :", data);
            return;
        }

        const container = d3.select("#wrapper");
        container.selectAll("*").remove();

        const width = 1600;
        const height = 1000;

        const svg = container.append("svg")
            .attr("viewBox", [0, 0, width, height])
            .style("width", "100%")
            .style("height", "90vh")
            .append("g")
            .attr("transform", "translate(80,40)");

        // Convertir data.nodes et data.edges en structure hiérarchique
        const nodeById = {};
        data.nodes.forEach(n => nodeById[n.id] = { ...n, children: [] });

        data.edges.forEach(e => {
            const parent = nodeById[e.from];
            const child = nodeById[e.to];
            if (parent && child) parent.children.push(child);
        });

        // Trouver la racine (aucun parent)
        const childIds = new Set(data.edges.map(e => e.to));
        const rootNode = data.nodes.find(n => !childIds.has(n.id));
        if (!rootNode) {
            console.error("❌ Racine introuvable dans les données");
            return;
        }

        const root = d3.hierarchy(nodeById[rootNode.id]);

        const treeLayout = d3.tree().size([height, width - 160]);
        treeLayout(root);

        // Liens
        svg.selectAll("path.link")
            .data(root.links())
            .join("path")
            .attr("class", "link")
            .attr("fill", "none")
            .attr("stroke", "#ccc")
            .attr("stroke-width", 2)
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x));

        // Noeuds
        const node = svg.selectAll("g.node")
            .data(root.descendants())
            .join("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`);

        node.append("circle")
            .attr("r", 5)
            .attr("fill", d => d.children ? "#555" : "#999");

        node.append("text")
            .attr("dy", "0.31em")
            .attr("x", d => d.children ? -10 : 10)
            .attr("text-anchor", d => d.children ? "end" : "start")
            .text(d => d.data.name || `ID ${d.data.id}`)
            .style("font", "12px sans-serif");

        console.log("✅ drawTree() terminé avec succès");
    } catch (err) {
        console.error("❌ Erreur drawTree():", err);
    }
}

// ===========================
// Nouvelle fonction wrapper qui choisit la bonne méthode d’affichage selon la forme des données
export async function renderFamilyTree(containerId, data) {
    if (data?.nodes && data?.edges) {
        console.log("➡️ Données au format {nodes, edges} détectées → drawTree()");
        await drawTree(data);
    } else {
        console.log("➡️ Données au format hiérarchique → initMainD3Tree()");
        initMainD3Tree(containerId, data);
    }
}

// ===========================
// Chargement automatique à l’ouverture de page
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById("wrapper");
    if (container) {
        try {
            const res = await fetch("/api/tree/tree-data");
            if (!res.ok) throw new Error("Données arbre introuvables");
            const data = await res.json();
            await renderFamilyTree("wrapper", data);
        } catch (err) {
            alert("Erreur lors du chargement de l’arbre généalogique.");
            console.error(err);
        }
    }
});

// ===========================
// Fonctions exportées restantes (zoom, export, recherche, chargement...)
export function zoomIn() {
    currentScale = Math.min(currentScale * 1.2, 4);
    // Note : variable svgRoot ou zoomBehavior non définie dans ta version, à intégrer si besoin
    // svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.05);
    // svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export async function loadTreeData(rootId) {
    const response = await fetch(`/api/person/api/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur lors du chargement des données");
    return await response.json();
}
