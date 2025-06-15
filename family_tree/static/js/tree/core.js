// static/js/tree/core.js
console.log("✔ core.js initialisé");
console.log("🧠 core.js chargé");
console.log("📦 [core.js] D3 dispo ?", window.d3, typeof d3);

const wrapper = document.getElementById("wrapper");
console.log("🔍 wrapper in core.js ?", wrapper);

import { transformDataForD3 } from '/static/js/tree/d3-tree.js';
import {
  debounce,
  throttle,
  exportPNG,
  exportSVG,
  toggleFullscreen,
  buildTreeFromEdges,
  centerTree,
  searchNode
} from '/static/js/tree/utils.js';

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
                .node circle { 
                    fill: #fff;
                    stroke: steelblue;
                    stroke-width: 2px;
                    r: 10px; /* Taille fixe des cercles */
                }
                .node text { 
                    font: 14px sans-serif; /* Texte plus grand */
                    font-weight: bold;
                }
                .link { 
                    fill: none; 
                    stroke: #666; /* Couleur plus visible */
                    stroke-width: 3px; /* Branches plus épaisses */
                    stroke-opacity: 0.8;
                }
                .tooltip { position: absolute; text-align: center; padding: 5px; font: 12px sans-serif; background: lightsteelblue; border: 1px solid #aaa; pointer-events: none; border-radius: 3px; }
        
                .tree-controls {
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    padding: 10px;
                    background: rgba(255, 255, 255, 0.9);
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                    z-index: 1000;
                }

                .tree-controls input[type="text"] {
                    padding: 6px 8px;
                    font-size: 14px;
                    border: 1px solid #aaa;
                    border-radius: 4px;
                }

                .tree-controls button {
                    padding: 6px 12px;
                    font-size: 14px;
                    border: none;
                    border-radius: 4px;
                    background-color: #3498db;
                    color: white;
                    cursor: pointer;
                }

                .tree-controls button:hover {
                    background-color: #2980b9;
                }

                select#rootSelector {
                    padding: 6px 8px;
                    font-size: 14px;
                    border: 1px solid #aaa;
                    border-radius: 4px;
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
/**
 * Fonction d’affichage D3.js (version nodes+edges avec sélection dynamique de racine)
 */
export async function drawTree(data) {
    console.log("✅ drawTree() started...");
    console.log("🟢 Données reçues pour dessiner l'arbre :", data);
    try {
        if (!data || !data.nodes || !data.edges) {
            console.error("❌ Données invalides pour drawTree:", data);
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

        // Indexation des noeuds
        const nodeById = {};
        data.nodes.forEach(n => nodeById[n.id] = { ...n, children: [] });

        // Construction des liens enfants
        data.edges.forEach(e => {
            const parent = nodeById[e.from];
            const child = nodeById[e.to];
            if (parent && child) parent.children.push(child);
        });

        // Détecter racines
        const rootCandidates = data.nodes.filter(n => {
            // Soit le noeud n'a pas de parent dans les edges
            // Soit ses parents ne sont pas dans les nodes (cas des données incomplètes)
            const parentEdges = data.edges.filter(e => e.to === n.id);
            return parentEdges.length === 0 || 
                    parentEdges.some(e => !data.nodes.some(n => n.id === e.from));
        });
        console.log("🌳 Ancêtres racines détectés :", rootCandidates.map(n => `${n.id} (${n.name || ''})`));

        if (rootCandidates.length === 0) {
            // Fallback: prendre le premier noeud disponible
            rootCandidates.push(data.nodes[0]);
            console.warn("⚠ Aucune racine trouvée, utilisation du premier noeud comme fallback");
        }


        // Ajouter sélecteur racine
        addRootSelector(rootCandidates, nodeById, data, svg, width, height);

    } catch (err) {
        console.error("❌ Erreur drawTree():", err);
    }
}

/**
 * Ajoute un sélecteur dynamique de racine à l’interface
 */
function addRootSelector(rootCandidates, nodeById, data, svg, width, height) {
    let selector = document.getElementById("rootSelector");
    if (!selector) {
        selector = document.createElement("select");
        selector.id = "rootSelector";
        selector.style.position = "absolute";
        selector.style.top = "10px";
        selector.style.left = "10px";
        selector.style.zIndex = "1000";
        document.body.appendChild(selector);
    }
    selector.innerHTML = ""; // Clear previous

    rootCandidates.forEach(n => {
        const opt = document.createElement("option");
        opt.value = n.id;
        opt.textContent = `${n.name || 'ID ' + n.id} (ID: ${n.id})`;
        selector.appendChild(opt);
    });

    selector.addEventListener("change", () => {
        renderTreeFromRoot(selector.value, nodeById, svg, width, height);
    });

    // Afficher le premier racine par défaut
    renderTreeFromRoot(selector.value || rootCandidates[0].id, nodeById, svg, width, height);
}

/**
 * Render tree à partir d’une racine choisie
 */
function renderTreeFromRoot(rootId, nodeById, svg, width, height) {
    if (!nodeById[rootId]) {
        console.error(`Noeud ${rootId} non trouvé dans nodeById`);
        return;
    }
    
    svg.selectAll("*").remove();
    const rootData = nodeById[rootId];
    const root = d3.hierarchy(rootData);

    // Ajustez ces valeurs pour contrôler l'espacement
    const nodeSize = 120; // Augmentez pour plus d'espace entre les niveaux
    const treeWidth = width - 200;

    // Configuration pour un arbre vertical avec meilleur espacement
    const treeLayout = d3.tree()
        .nodeSize([nodeSize, treeWidth / 3]) // [hauteur, largeur] entre nœuds
        .separation((a, b) => 1.2); // Espace supplémentaire entre frères

    treeLayout(root);

    // Liens verticaux avec ajustement de la courbure
    const linkGenerator = d3.linkVertical()
        .x(d => d.x)
        .y(d => d.y);

    svg.selectAll("path.link")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("stroke-width", 3) // Branches plus épaisses
        .attr("d", linkGenerator);

    // Noeuds avec taille augmentée
    const node = svg.selectAll("g.node")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`);

    node.append("circle")
        .attr("r", 10) // Taille des cercles augmentée
        .attr("fill", d => d.children ? "#555" : "#999")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2);

    // Texte plus grand et mieux positionné
    node.append("text")
        .attr("dy", ".35em")
        .attr("x", d => d.children ? -15 : 15)
        .style("text-anchor", d => d.children ? "end" : "start")
        .style("font-size", "14px") // Taille de police augmentée
        .style("font-weight", "bold")
        .text(d => d.data.name);

    // Ajustement du viewBox pour mieux contenir l'arbre
    const bounds = svg.node().getBBox();
    svg.attr("viewBox", `${bounds.x-20} ${bounds.y-20} ${bounds.width+40} ${bounds.height+40}`);
}
// ===========================
// Nouvelle fonction wrapper qui choisit la bonne méthode d’affichage selon la forme des données
export async function renderFamilyTree(containerId, data) {
    console.log("✅ D3 chargé :", typeof d3); 
    console.log("📌 D3 version :", d3.version);
    console.log("🛠 D3 fonctions : ", Object.keys(d3));
    try {
    d3.select('body').append('div').text('D3 fonctionne!');
    console.log('✅ Test D3 réussi');
    } catch (e) {
    console.error('❌ Échec test D3:', e);
    }

    if (data?.nodes && data?.edges) {
        console.log("➡️ Données au format {nodes, edges} détectées → drawTree()");
        await drawTree(data);
    } else {
        console.log("➡️ Données au format hiérarchique → initMainD3Tree()");
        initMainD3Tree(containerId, data);
    }
}

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
