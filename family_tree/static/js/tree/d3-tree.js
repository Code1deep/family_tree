// static/js/tree/d3-tree.js
import { debounce, downloadURL, toggleFullscreen, centerTree } from './utils.js';
import { openModal } from '/static/js/modal.js';

/** CSS intégré dynamiquement */
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
            .html(`
                .link { fill: none; stroke: #ccc; stroke-width: 1.5px; }
                .node circle { fill: #999; stroke: #555; stroke-width: 1.5px; }
                .node text { font: 10px sans-serif; }
            `);
    }

    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`⏭️ Conteneur introuvable : #${containerId}`);
        return;
    }

    container.innerHTML = '';
    const margin = { top: 50, right: 120, bottom: 50, left: 120 };
    let width = container.clientWidth - margin.left - margin.right;
    let height = container.clientHeight - margin.top - margin.bottom;

    const svg = d3.select(`#${containerId}`).append("svg")
        .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .attr("preserveAspectRatio", "xMidYMid meet");

    const gZoom = svg.append("g");
    const g = gZoom.append("g").attr("class", "tree-group");

    const zoom = d3.zoom()
        .scaleExtent([0.1, 3])
        .on("zoom", event => g.attr("transform", event.transform));
    svg.call(zoom);

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

    node.append("text")
        .attr("dy", "2.5em")
        .attr("x", 25)
        .style("cursor", "pointer")
        .style("fill", "#007bff")
        .style("text-decoration", "underline")
        .text("👁 Voir les détails")
        .on("click", showPersonDetails);

    centerTree(g, container, svg);
    setupTreeSearch(root, g);
    setupExportButtons(containerId);
    setupFullscreen(container);
    setupResizeHandler(() => initSubD3Tree(containerId, data));
    setupCenterButton(containerId, g, svg);
}

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

function setupResizeHandler(redrawFn) {
    window.addEventListener("resize", debounce(() => redrawFn(), 300));
}

function setupCenterButton(containerId, g, svg) {
    const btn = document.getElementById('center-tree');
    if (!btn) return;

    btn.addEventListener("click", () => {
        const bbox = g.node()?.getBBox?.();
        if (!bbox) return;
        const x = bbox.x + bbox.width / 2;
        const y = bbox.y + bbox.height / 2;

        const container = document.getElementById(containerId);
        const dx = container.clientWidth / 2 - x;
        const dy = container.clientHeight / 2 - y;

        svg.transition()
            .duration(750)
            .call(
                d3.zoom().transform,
                d3.zoomIdentity.translate(dx, dy).scale(1)
            );
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

export function transformDataForD3(rawData) {
    return d3.hierarchy(rawData);
}

// Les fonctions suivantes sont conservées si besoin futur, mais non utilisées dans ce fichier.
/*
function update(source) {}
function zoomed(event) {}
*/
