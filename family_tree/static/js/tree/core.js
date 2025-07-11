// static/js/tree/core.js

const wrapper = document.getElementById("wrapper");
console.log("🔍 wrapper in core.js ?", wrapper);
import { setupAdvancedSearch } from './utils.js';
import { setupGenerationJump } from './d3-tree.js';
import { transformDataForD3 } from './d3-tree.js';
console.log("✅✅✅ VERSION core.js ACTIVE ✅✅✅");
console.log("✔ core.js initialisé");
console.log("📦 [core.js] D3 dispo ?", window.d3, typeof d3);
import { setupTreeControls } from './controls.js';
import {
  centerTree,
  exportPNG,
  exportSVG,
  toggleFullscreen,
  searchNode
} from './utils.js';

let svgRootGlobal = null; // Exposé pour que SearchHandler l'utilise

/**
 * Affiche l'arbre à partir de données au format { nodes, edges }.
 * @param {Object} data 
 */

let currentScale = 1;

// Définition des couleurs pour chaque génération (0 à 9)

const generationColors = [
  "#F1C40F", // Jaune clair
  "#E67E22", // Orange clair
  "#1ABC9C", // Turquoise clair
  "#F39C12", // Orange doux
  "#2ECC71", // Vert clair
  "#c9f8fc", // Bleu clair
  "#fabebe", // Violet clair
  "#f76c59", // Rouge vif mais lumineux
  "#d3fcbd", // Gris clair
  "#b9c26b"  // Bleu pastel
];


const textColors = [
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
  "#1754e3", // 
];

// ===========================
// Fonction principale D3.js
// ===========================
export function initMainD3Tree(containerId, data) {
  console.log("🚀 Initialisation de l'arbre principal...");

  const margin = { top: 50, right: 200, bottom: 50, left: 200 };
  const width = 2000 - margin.left - margin.right;
  const height = 1200 - margin.top - margin.bottom;

  const container = d3.select(`#${containerId}`);
  container.selectAll("*").remove();

  // Ajout des contrôles UI
    // 1) Insère le HTML UNE FOIS
    container.insert("div", ":first-child")
        .attr("class", "tree-controls")
        .html(`
            <input id="treeSearch" placeholder="Rechercher une personne..." />
            <button id="centerBtn">Centrer</button>
            <button id="pngBtn">Export PNG</button>
            <button id="svgBtn">Export SVG</button>
            <button id="fullscreenBtn">Plein écran</button>
            <label for="goto-generation">Aller à la génération :</label>
            <select id="goto-generation"></select>
            <button id="genBtn">Aller</button>
        `);

    // Création du SVG et du groupe interne <g>
    const svgRoot = container.append("svg")
        .attr("viewBox", [0, 0, width + margin.left + margin.right, height + margin.top + margin.bottom])
        .style("width", "100%")
        .style("height", "90vh");

    const svg = svgRoot.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Définir et activer le zoom
    const zoom = d3.zoom().on("zoom", (event) => {
        svg.attr("transform", event.transform);
    });
    svgRoot.call(zoom);

    // Préparer la hiérarchie et le layout
    const treeLayout = d3.tree().nodeSize([30, 300]);
    const root = d3.hierarchy(data);
    root.x0 = 0;
    root.y0 = 0;

    treeLayout(root);
    root.descendants().forEach(d => d.y = d.depth * 180);

    // Ton update() doit exister quelque part
    update(root);

    // ⏩ Appel correct du jump avec le bon zoom et g
    setupGenerationJump(root, svg, zoom);

  function update(source) {
  // 1️⃣ (Re)calcule le layout :
  const treeData = treeLayout(root);

  // 2️⃣ Liste des nœuds et liens :
  const nodes = treeData.descendants();
  const links = treeData.links();

  // 3️⃣ Définit y en fonction de la profondeur :
  nodes.forEach(d => d.y = d.depth * 180);

  // 4️⃣ Affiche les positions :
  console.log("✅ Nodes après layout :", nodes.map(d => [d.data.name, d.x, d.y]));
    
    const node = svg.selectAll("g.node")
      .data(nodes, d => d.data.id);

    const nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", d => `translate(${source.y0},${source.x0})`)
      .on("click", (event, d) => {
        if (d.children) {
          d.children = null;
        } else if (d._children) {
          d.children = d._children;
          d._children = null;
        } else {
          window.location.href = `/api/person/person/${d.data.id}`;
        }
        update(d);
      });

    nodeEnter.append("circle")
      .attr("r", 4)
      .style("fill", d => generationColors[d.depth % generationColors.length]);

    nodeEnter.append("text")
      .attr("dy", 3)
      .attr("x", d => d.children ? -10 : 10)
      .style("text-anchor", d => d.children ? "end" : "start")
      .style("fill", d => textColors[d.depth % textColors.length])
      .text(d => d.data.name);

    node.merge(nodeEnter).transition().duration(500)
      .attr("transform", d => `translate(${d.y},${d.x})`);

    node.exit().remove();

    const link = svg.selectAll("path.link")
      .data(links, d => d.target.data.id);

    link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x));

    link.merge(link).transition().duration(500)
      .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x));

    link.exit().remove();
  }

    // Setup UI
    // Ajoutez en tête du fichier (avec les autres imports)
    async function checkFullscreenPermission() {
        try {
            if (navigator.permissions?.query) {
                const permissionStatus = await navigator.permissions.query({name: 'fullscreen'});
                permissionStatus.onchange = () => console.log('Permission fullscreen:', permissionStatus.state);
                return permissionStatus.state === 'granted';
            }
            return true; // Fallback pour les navigateurs sans API Permissions
        } catch (err) {
            console.warn("Erreur de vérification des permissions:", err);
            return true;
        }
    }

    // Puis modifiez la section des contrôles UI :
    d3.select("#centerBtn").on("click", () => centerTree(svg));
    d3.select("#pngBtn").on("click", () => exportPNG(containerId));
    d3.select("#svgBtn").on("click", () => exportSVG(containerId));
    d3.select("#fullscreenBtn").on("click", async () => {
        if (await checkFullscreenPermission()) {
            toggleFullscreen(containerId);
        } else {
            console.warn("Plein écran bloqué par les permissions");
            // Optionnel : Afficher un message à l'utilisateur
            alert("Veuillez autoriser le plein écran dans les paramètres de votre navigateur");
        }
    });

    console.log("Je passe tree ?", tree);
    setupAdvancedSearch(root, svgRoot, zoom, width, height, update, treeLayout);
    return { root, svgRoot, zoom, width, height, update };

}

// ===========================
// Export de secours pour structure edges/nodes
// ===========================
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

        const svgRoot = container.append("svg")
            .attr("viewBox", [0, 0, width, height])
            .style("width", "100%")
            .style("height", "90vh")
            //.attr("class", "tree-group")

        const g = svgRoot.append("g")
            .attr("class", "tree-group")
            .attr("transform", "translate(80,40)");

        const baseTranslate = d3.zoomIdentity.translate(80, 40);
        console.log("🔎 baseTranslate dans drawTree(data) =", baseTranslate);

        // Ton zoom setup
        const zoom = d3.zoom().on("zoom", (event) => {
        g.attr("transform", event.transform);
        });
        svgRoot.call(zoom).call(zoom.transform, baseTranslate);

        // ✅ Expose globalement pour SearchHandler
        window.svgRoot = g;
        svgRootGlobal = g;
        console.log("✅ svgRoot exposé :", window.svgRoot);

        // Indexation des noeuds
        const nodeById = {};
        data.nodes.forEach(n => nodeById[n.id] = { ...n, children: [] });

        // Construction des liens enfants
        // Créer les relations
        data.edges.forEach(e => {
            const parent = nodeById[e.from];
            const child = nodeById[e.to];
            if (parent && child) {
            parent.children.push(child);
            }
        });

        // Détecter racines
        const rootCandidates = data.nodes.filter(n => {
        const parentEdges = data.edges.filter(e => e.to === n.id);
        return parentEdges.length === 0 ||
                parentEdges.some(e => !data.nodes.some(n2 => n2.id === e.from));
        });

        console.log("🌳 Ancêtres racines détectés :", rootCandidates);

        if (rootCandidates.length === 0) {
        if (data.nodes.length > 0) {
            rootCandidates.push(data.nodes[0]);
            console.warn("⚠ Aucune racine trouvée, fallback = premier noeud");
        } else {
            console.error("⛔ Aucun noeud dans data.nodes → arrêt !");
            return;
        }
        }

        if (!rootCandidates[0]) {
        console.error("⛔ Fallback racine = undefined !");
        return;
        }

        // Ajouter sélecteur racine
        addRootSelector(rootCandidates, nodeById, data, g, width, height, zoom);
    
        const selector = document.getElementById("rootSelector");
        if (!selector) {
          console.warn("⚠ Selector non trouvé");
          return;
        }
    
        // Fonction update : réutilise renderTreeFromRoot
        const update = () => renderTreeFromRoot(selector.value, nodeById, g, width, height, zoom);
    
        // Premier rendu
        renderTreeFromRoot(selector.value || rootId, nodeById, g, width, height, zoom);
    
        // ⚡ Important : Construire le vrai root.hierarchy pour la recherche
        const rootData = nodeById[selector.value || rootId];
        const root = d3.hierarchy(rootData);
    
        // 🔑 Brancher la recherche ici
        //console.log("Je passe tree ?", tree);
        //setupAdvancedSearch(root, svgRoot, zoom, width, height, update, treeLayout);
        //return { root, svgRoot, zoom, width, height, update };
        //return { g, svgRoot, zoom, baseTranslate };
      } catch (err) {
        console.error("❌ Erreur drawTree():", err);
        throw err;
      }
    }
//Ajoute un sélecteur dynamique de racine à l'interface
function addRootSelector(rootCandidates, nodeById, data, g, width, height, zoom) {
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
        opt.textContent = `${n.name} (ID:${n.id})`;
        selector.appendChild(opt);
    });

    selector.addEventListener("change", () => {
        renderTreeFromRoot(selector.value, nodeById, g, width, height, zoom);
    });

    // Afficher le premier racine par défaut
    renderTreeFromRoot(selector.value || rootCandidates[0].id, nodeById, g, width, height, zoom);
}
/* Render tree à partir d'une racine choisie*/
function renderTreeFromRoot(rootId, nodeById, g, width, height, zoom) {
    if (!nodeById[rootId]) return;
        g.selectAll("*").remove();
    const rootData = nodeById[rootId];
    const root = d3.hierarchy(rootData);
    // Configuration VERTICALE reglage distance entre noeuds horizontal et vertical
    const nodeRadius = 55;
    const verticalSpacing = 350; // Espace vertical plus large
    const horizontalSpacing = 250; // Espace horizontal suffisant
    const treeLayout = d3.tree()
        //.size([height - 200, width - 200]) // [height, width] pour vertical
        .nodeSize([verticalSpacing, horizontalSpacing]);
    treeLayout(root);
    // Centrage HORIZONTAL
    const minX = d3.min(root.descendants(), d => d.x);
    const maxX = d3.max(root.descendants(), d => d.x);
    const xOffset = (width - (maxX - minX)) / 2 - minX;
    // Liens VERTICAUX (inversion x/y)
    g.selectAll("path.link")
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
    const node = g.selectAll("g.node")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x + xOffset},${d.y})`);
    // Cercles de 55px
    node.append("circle")
        .attr("r", nodeRadius)
        .attr("class", d => {
            console.log(`📌 Nœud ${d.data.name} (ID:${d.data.id}) - Profondeur: ${d.depth}`);
            return `ft-node ft-gener-${d.depth}`; // Utilisation de depth pour la génération
        })
        .attr("fill", d => {
            const colorIndex = d.depth % generationColors.length;
            const color = generationColors[colorIndex];
            console.log(`🎨 Nœud ${d.data.name} - Profondeur ${d.depth} → Couleur ${color} (index ${colorIndex})`);
            return color;
        })
        .attr("stroke", "steelblue")
        .attr("stroke-width", 5)
        .style("cursor", "pointer")   // ✅ Visuel
        .on("click", (event, d) => {  // ✅ Action click
            console.log("💥 CLICK TEST a partir d core.js !", d);
            opt.textContent = `${n.name || 'ID ' + n.id} (ID: ${n.id})`;
            window.location.href = `/api/person/person/${d.data.id}`;
        });
    // Texte
    node.append("text")
        .attr("dy", ".35em")
        .attr("x", d => d.children ? -nodeRadius-10 : nodeRadius+10)
        .style("text-anchor", d => d.children ? "end" : "start")
        .style("font-size", "24px")
        .style("fill", d => {
            const color = textColors[d.depth % textColors.length];
            console.log(`🖋️ [render] Texte ${d.data.name} - Profondeur ${d.depth} → Couleur ${color}`);
            return color;
        }) // Couleur par génération
        .style("paint-order", "stroke")
        .style("stroke", "#000")           // contour noir
        .style("stroke-width", "2px")      // épaisseur du contour
        .style("stroke-linejoin", "round")
        .text(d => d.data.name);

            // ✅ CLIC actif sur le groupe entier (nœud)
    node.on("click", (event, d) => {
        console.log(`👆 Clic sur ${d.data.name} (ID: ${d.data.id}) → Redirection...`);
        window.location.href = `/api/person/person/${d.data.id}`;
    });

    // Ajustement viewport
    const padding = 50;
    g.attr("viewBox", `0 0 ${width} ${height}`)
       .attr("preserveAspectRatio", "xMidYMid meet");

    // ✅ Setup du jump pour cette racine visible
    setupGenerationJump(root, g, zoom);
}
// Nouvelle fonction wrapper qui choisit la bonne méthode d'affichage selon la forme des données
// Wrapper pour choisir le bon affichage
export async function renderFamilyTree(containerId, data) {
    
    console.log("🚀 renderFamilyTree() appelée");
    console.log("📦 containerId =", containerId);
    console.log("📦 data =", data);

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
        const { g, svgRoot, zoom, baseTranslate } = await drawTree(data);
        return { g, svgRoot, zoom, baseTranslate };
    } else {
        console.log("➡️ Données au format hiérarchique → initMainD3Tree()");
        return initMainD3Tree(containerId, data);
    }
}

export async function loadTreeData(rootId) {
    const response = await fetch(`/api/person/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur lors du chargement des données");
    return await response.json();
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
