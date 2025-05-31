// static/js/tree/d3-tree.js
import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { centerTree } from './utils.js';
import { debounce } from './utils.js';

// Injecte du CSS dans le DOM
function injectTreeStyles() {
    const style = document.createElement("style");
    style.textContent = `
        .node circle {
            fill: #fff;
            stroke: steelblue;
            stroke-width: 2.5px;
        }
        .node text {
            font: 14px sans-serif;
        }
        .node.highlighted circle {
            fill: orange;
        }
        .link {
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }
    `;
    document.head.appendChild(style);
}

export function initD3Tree(containerId, data) {
    injectTreeStyles();

    const margin = { top: 50, right: 120, bottom: 50, left: 120 };
    const width = 1600 - margin.left - margin.right;
    const height = 1000 - margin.top - margin.bottom;

    const svgRoot = d3.select(`#${containerId}`).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    const svg = svgRoot
        .call(d3.zoom().scaleExtent([0.1, 3]).on("zoom", (event) => {
            g.attr("transform", event.transform);
        }))
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const treeLayout = d3.tree().size([height, width]);
    const root = d3.hierarchy(data);
    treeLayout(root);

    const g = svg.append("g");

    // Liens entre noeuds
    g.selectAll(".link")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    // Noeuds
    const node = g.selectAll(".node")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle")
        .attr("r", 6);

    node.append("text")
        .attr("dy", 3)
        .attr("x", d => d.children ? -12 : 12)
        .style("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name);

    setupTreeSearch(root);
}

function setupTreeSearch(rootNode) {
    const input = document.getElementById('tree-search');
    if (!input) return;

    input.addEventListener('input', debounce((e) => {
        const query = e.target.value.toLowerCase();
        d3.selectAll(".node")
            .classed("highlighted", d => d.data.name.toLowerCase().includes(query));
    }, 300));
}

export function exportAsSVG(containerId) {
    const svgElement = document.querySelector(`#${containerId} svg`);
    const serializer = new XMLSerializer();
    const svgData = serializer.serializeToString(svgElement);
    const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tree_export.svg";
    a.click();
    URL.revokeObjectURL(url);
}

export function exportAsPNG(containerId) {
    const svgElement = document.querySelector(`#${containerId} svg`);
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);

    const image = new Image();
    const canvas = document.createElement("canvas");
    const bbox = svgElement.getBBox();
    canvas.width = bbox.width + 100;
    canvas.height = bbox.height + 100;
    const ctx = canvas.getContext("2d");

    image.onload = () => {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 50, 50);
        const png = canvas.toDataURL("image/png");
        const a = document.createElement("a");
        a.href = png;
        a.download = "tree_export.png";
        a.click();
        URL.revokeObjectURL(url);
    };
    image.src = url;
}

    function update(source) {
        // Logique de mise à jour optimisée
    }

    function zoomed(event) {
        svg.attr("transform", event.transform);
    }

    // Initial render
    update(root);

    centerTree(svg, document.getElementById(containerId));
