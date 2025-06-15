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

// Définition des couleurs pour chaque génération (0 à 9)
const generationColors = [
    "#3498db", // Génération 0 (bleu)
    "#e74c3c", // Génération 1 (rouge)
    "#2ecc71", // Génération 2 (vert)
    "#9b59b6", // Génération 3 (violet)
    "#f39c12", // Génération 4 (orange)
    "#1abc9c", // Génération 5 (turquoise)
    "#d35400", // Génération 6 (orange foncé)
    "#7f8c8d", // Génération 7 (gris)
    "#8e44ad", // Génération 8 (violet foncé)
    "#27ae60"  // Génération 9 (vert foncé)
];

// Ajout en haut du fichier
console.log("🎨 Initialisation des couleurs de génération");
console.log("🌈 generationColors:", generationColors);
d3.select("head").append("style")
    .html(`
        .ft-node {
            fill: red !important;
        }
    `);
// ===========================
// Fonction principale d'affichage D3.js (version hiérarchique)
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
                    fill: #fff !important;
                    stroke: steelblue !important;
                    stroke-width: 5px !important;
                    r: 55px !important;
                }
                .node text {
                    font: 24px 'Arial', sans-serif !important;
                    font-weight: bold !important;
                    fill: #333 !important;
                }
                .link {
                    stroke: #666 !important;
                    stroke-width: 5px !important;
                    stroke-opacity: 0.9 !important;
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

    const hierarchyData = d3.hierarchy(data);
    setNodeLevels(hierarchyData); // `root` est ton nœud racine D3

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

    function setNodeLevels(node, level = 0) {
        node.level = level;
        if (node.children) {
            node.children.forEach(child => setNodeLevels(child, level + 1));
        }
    }

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
            .attr("class", d => {
                console.log(`📌 [init] Nœud ${d.data.name} (ID:${d.data.id}) - Profondeur: ${d.depth}`);
                return `ft-node ft-gener-${d.depth}`;
            })  // Utilisation de depth pour la génération
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .style('fill', d => {
                const colorIndex = d.depth % generationColors.length;
                const color = generationColors[colorIndex];
                console.log(`🎨 [init] Nœud ${d.data.name} - Profondeur ${d.depth} → Couleur ${color} (index ${colorIndex})`);
                return color;
            });

        nodeEnter.append('text')
            .attr("dy", 3)
            .attr("x", d => d._children ? -10 : 10)
            .style("text-anchor", d => d._children ? "end" : "start")
            .text(d => d.data.name);

        const nodeUpdate = nodeEnter.merge(node);
        nodeUpdate.transition().duration(500).attr("transform", d => `translate(${d.y},${d.x})`);
        nodeUpdate.select('circle').attr('r', 4).style('fill', d => generationColors[d.depth % generationColors.length]);

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
 * Fonction d'affichage D3.js (version nodes+edges avec sélection dynamique de racine)
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
 * Ajoute un sélecteur dynamique de racine à l'interface
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
 * Render tree à partir d'une racine choisie
 */
function renderTreeFromRoot(rootId, nodeById, svg, width, height) {
    if (!nodeById[rootId]) return;
    
    svg.selectAll("*").remove();
    const rootData = nodeById[rootId];
    const root = d3.hierarchy(rootData);

    // Configuration VERTICALE
    const nodeRadius = 55;
    const verticalSpacing = 200;
    const horizontalSpacing = 250;

    const treeLayout = d3.tree()
        .size([height - 200, width - 200]) // [height, width] pour vertical
        .nodeSize([verticalSpacing, horizontalSpacing]);

    treeLayout(root);

    // Centrage HORIZONTAL
    const minX = d3.min(root.descendants(), d => d.x);
    const maxX = d3.max(root.descendants(), d => d.x);
    const xOffset = (width - (maxX - minX)) / 2 - minX;

    // Liens VERTICAUX (inversion x/y)
    svg.selectAll("path.link")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("d", d3.linkVertical()
            .x(d => d.x + xOffset) // Position horizontale centrée
            .y(d => d.y)); // Position verticale

    // Dans la fonction renderTreeFromRoot, avant la création des nœuds
    console.log("🖌 Préparation des couleurs pour les nœuds");
    console.log("📊 Profondeur de la racine:", root.depth);
    console.log("📊 Descendants:", root.descendants().length);

    // Noeuds VERTICAUX
    const node = svg.selectAll("g.node")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x + xOffset},${d.y})`); // Inversion x/y

    // Cercles de 55px
    node.append("circle")
        .attr("r", nodeRadius)
        .attr("class", d => {
            console.log(`📌 Nœud ${d.data.name} (ID:${d.data.id}) - Profondeur: ${d.depth}`);
            return `ft-node ft-gener-${d.depth}`;  // Utilisation de depth pour la génération
        })
        .attr("fill", d => {
            const colorIndex = d.depth % generationColors.length;
            const color = generationColors[colorIndex];
            console.log(`🎨 Nœud ${d.data.name} - Profondeur ${d.depth} → Couleur ${color} (index ${colorIndex})`);
            return color;
        })
        .attr("stroke", "steelblue")
        .attr("stroke-width", 5);

    // Texte
    node.append("text")
        .attr("dy", ".35em")
        .attr("x", d => d.children ? -nodeRadius-10 : nodeRadius+10)
        .style("text-anchor", d => d.children ? "end" : "start")
        .style("font-size", "24px")
        .text(d => d.data.name);

    // Ajustement viewport
    const padding = 50;
    svg.attr("viewBox", `0 0 ${width} ${height}`)
       .attr("preserveAspectRatio", "xMidYMid meet");
}

// ===========================
// Nouvelle fonction wrapper qui choisit la bonne méthode d'affichage selon la forme des données
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
