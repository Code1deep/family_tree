// static/js/tree/d3-tree.js
import { debounce, downloadURL, toggleFullscreen } from '/static/js/tree/utils.js';
import { openModal } from '/static/js/modal.js';

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
            .html(`
                .link { fill: none; stroke: #ccc; stroke-width: 1.5px; }
                .node circle { stroke: #555; stroke-width: 1.5px; }
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

    const treeLayout = d3.tree().size([height, width]);  // [y, x] pour vertical
    const root = d3.hierarchy(data);
    treeLayout(root);

    g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.linkVertical()
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

    centerTree(g, container, zoom);
    setupTreeSearch(root, g);
    setupExportButtons(containerId);
    setupFullscreen(container);
    setupResizeHandler(() => initSubD3Tree(containerId, data));
    setupCenterButton(containerId, g, svg, zoom);
}

function setupTreeSearch(root, g) {
    const input = document.getElementById('tree-search');
    if (!input) return;

    input.addEventListener('input', debounce(() => {
        const query = input.value.trim().toLowerCase();
        g.selectAll('.node')
            .classed('node--highlight', d => d.data.name.toLowerCase().includes(query));
    }, 300));
}

function setupResizeHandler(redrawFn) {
    window.addEventListener("resize", debounce(() => redrawFn(), 300));
}

export function setupCenterButton(containerId, g, svg, zoom) {
    const btn = document.getElementById("centerBtn");
    if (!btn) {
        console.warn("⚠️ Bouton centerBtn introuvable");
        return;
    }

    btn.addEventListener("click", () => {
        console.log("🎯 Clic bouton : Centrer arbre");
        
        const container = document.getElementById(containerId);
        if (!g || !container || !zoom) {
            console.error("❌ Paramètres manquants pour centrer l'arbre");
            return;
        }

        const bbox = g.node().getBBox();
        if (!bbox || isNaN(bbox.width) || isNaN(bbox.height)) {
            console.error("❌ BBox invalide ou introuvable");
            return;
        }

        const width = container.clientWidth;
        const height = container.clientHeight;

        const scale = Math.min(width / bbox.width, height / bbox.height, 1);
        const translate = [
            (width - bbox.width * scale) / 2 - bbox.x * scale,
            (height - bbox.height * scale) / 2 - bbox.y * scale
        ];

        svg.transition().duration(750)
            .call(zoom.transform, d3.zoomIdentity.translate(...translate).scale(scale));
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
