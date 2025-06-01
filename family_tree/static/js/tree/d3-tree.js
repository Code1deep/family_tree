// static/js/tree/d3-tree.js
import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { debounce } from './utils.js';
import { openModal } from '/static/js/modal.js';

// Injecte du CSS dans le DOM
/** CSS directement intégré */
const style = document.createElement("style");
style.innerHTML = `
.node circle {
    fill: #fff;
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
`;
document.head.appendChild(style);

function showPersonDetails(d) {
    const p = d.data;  // Le JSON du nœud
    const photo = p.photo || "/static/img/default.png";
    const bio = p.data.bio || "Aucune biographie disponible";
    const mother = p.data.mother || "Inconnue";
    const father = p.data.father || "Inconnu";

    const html = `
        <img src="${photo}" alt="Photo de ${p.name}">
        <h2>${p.name}</h2>
        <p><strong>Biographie :</strong> ${bio}</p>
        <p><strong>Parents :</strong> ${mother} & ${father}</p>
    `;
    openModal(html);
}

/** Fonction principale */
export function initD3Tree(containerId, data) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // reset
    const margin = { top: 50, right: 120, bottom: 50, left: 120 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    const svg = d3.select(`#${containerId}`).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .call(d3.zoom().scaleExtent([0.1, 3]).on("zoom", (event) => {
            g.attr("transform", event.transform);
        }))
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const g = svg.append("g");

    const treeLayout = d3.tree().size([height, width]);
    const root = d3.hierarchy(data);
    treeLayout(root);

    g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle").attr("r", 6);
    node.append("text")
        .attr("dy", 3)
        .attr("x", d => d.children ? -10 : 10)
        .style("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name);
    
        // Ajoute dans le nœud SVG le bouton
    nodeEnter.append("text")
        .attr("dy", "2.5em")
        .attr("x", 25)
        .style("cursor", "pointer")
        .style("fill", "#007bff")
        .style("text-decoration", "underline")
        .text("👁 Voir les détails")
        .on("click", showPersonDetails);

    centerTree(svg, container);

    // Setup interactivité
    setupTreeSearch(root, g);
    setupExportButtons(containerId);
    setupFullscreen(container);
}

/** Recherche */
function setupTreeSearch(root, g) {
    const input = document.getElementById('tree-search');
    if (!input) return;
    input.addEventListener('input', debounce(() => {
        const query = input.value.trim().toLowerCase();
        g.selectAll('.node').classed('node--highlight', false);
        if (query) {
            g.selectAll('.node')
                .filter(d => d.data.name.toLowerCase().includes(query))
                .classed('node--highlight', true);
        }
    }, 300));
}

/** Centrage automatique */
function centerTree(svg, container) {
    const g = svg.select('g');
    const bbox = g.node().getBBox();
    const x = bbox.x + bbox.width / 2;
    const y = bbox.y + bbox.height / 2;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    const dx = containerWidth / 2 - x;
    const dy = containerHeight / 2 - y;

    g.transition().duration(500)
        .attr("transform", `translate(${dx},${dy})`);
}

/** Export PNG & SVG */
function setupExportButtons(containerId) {
    const exportSvgBtn = document.getElementById("export-svg");
    const exportPngBtn = document.getElementById("export-png");

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
    let source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadURL(url, "genealogy-tree.svg");
}

function exportAsPNG(containerId) {
    const svg = document.querySelector(`#${containerId} svg`);
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svg);

    const canvas = document.createElement("canvas");
    const bbox = svg.getBBox ? svg.getBBox() : { width: 1200, height: 800 };
    canvas.width = bbox.width + 200;
    canvas.height = bbox.height + 200;
    const ctx = canvas.getContext("2d");

    const img = new Image();
    const svgBlob = new Blob([svgString], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);
    img.onload = function () {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 100, 100);
        URL.revokeObjectURL(url);
        const imgURI = canvas.toDataURL("image/png").replace("image/png", "octet/stream");
        downloadURL(imgURI, "genealogy-tree.png");
    };
    img.src = url;
}

/** Utils */
function downloadURL(data, filename) {
    const a = document.createElement("a");
    a.href = data;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function update(source) {
    // Logique de mise à jour optimisée
}

function zoomed(event) {
    svg.attr("transform", event.transform);
}

    // Initial render
    update(root);
