// static/js/tree/controls.js
console.log("✔ core.js initialisé");
console.log("🧠 core.js chargé");
console.log("📦 [core.js] D3 dispo ?", window.d3, typeof d3);

// const wrapper = document.getElementById("wrapper");
// console.log("🔍 wrapper in core.js ?", wrapper);

import { transformDataForD3 } from '/static/js/tree/d3-tree.js';

  
/**
 * Attache les contrôles de l’arbre généalogique.
 * @param {Object} params - Paramètres nécessaires.
 * @param {d3.Selection} params.container - Conteneur D3 du SVG principal.
 * @param {d3.Selection} params.svgRoot - Groupe `<g>` D3 contenant l’arbre.
 * @param {HTMLElement} params.svgNode - Élément DOM <svg>.
 * @param {Object} params.root - Donnée racine D3.
 * @param {Function} [params.update] - Fonction update() si nécessaire.
 */
import { debounce, centerTree, exportPNG, exportSVG, toggleFullscreen, searchNode } from "./utils.js";
/**
 * Classe gestionnaire de recherche D3.
 */
class SearchHandler {
  constructor(svgRoot) {
    this.svgRoot = svgRoot;
  }

  /**
   * Réinitialise les styles de tous les textes de nœuds.
   */
  resetSearch() {
    if (!this.svgRoot) {
      console.warn("⚠️ Aucun svgRoot pour resetSearch");
      return;
    }
    this.svgRoot.selectAll("g.node text")
      .style("font-weight", "normal")
      .style("fill", "black");
  }

  /**
   * Exécute une recherche : reset + recherche.
   * @param {string} term - Texte à chercher.
   */
  executeSearch(term) {
    console.log("🔍 executeSearch →", term);
    this.resetSearch();
    if (term) {
      searchNode(term, this.svgRoot);
    }
  }

  /**
   * Écouteur pour l'événement input.
   * @param {Event} event
   */
  handleEvent(event) {
    const term = event.target.value.trim();
    console.log("🔍 Recherche en cours :", term);
    this.executeSearch(term);
  }
}
/**
 * Configure tous les contrôles de l'arbre généalogique.
 * @param {Object} params
 * @param {d3.Selection} params.container - Conteneur D3 du SVG.
 * @param {d3.Selection} params.svgRoot - Groupe `<g>`.
 * @param {HTMLElement} params.svgNode - Élément `<svg>`.
 * @param {Object} params.root - Données racine.
 * @param {Function} [params.update] - Fonction update().
 * @param {d3.Selection} params.g - Groupe principal.
 * @param {d3.ZoomBehavior} params.zoom - Comportement zoom.
 * @param {Object} params.baseTranslate - d3.zoomIdentity de base.
 */
export function setupTreeControls({
  container,
  svgRoot,
  svgNode,
  root,
  update,
  g,
  zoom,
  baseTranslate
}) {
  console.log("⚙️ setupTreeControls → container :", container);
  console.log("⚙️ setupTreeControls → svgNode :", svgNode);
  console.log("⚙️ setupTreeControls → baseTranslate :", baseTranslate);
  console.log("⚙️ setupTreeControls → zoom :", zoom);

  if (!container) {
    console.error("❌ ERREUR : Pas de container transmis.");
    return;
  }
 }
  // ✅ Boutons de base avec `g` & `zoom`
if (!window.setupTreeControls) { 
function setupTreeControls({ container, svgRoot, svgNode, root, update }) {
    if (!svgNode) {
        console.error("❌ Aucun élément SVG trouvé pour les contrôles.");
        return;
    }
    console.log("⚙️ setupTreeControls → container :", container);
    console.log("⚙️ baseTranslate :", baseTranslate);
    const parent = svgNode.parentElement;
    const searchHandler = new SearchHandler(svgRoot);

    // ✅ Boutons reliés avec le VRAI container et baseTranslate
    const controls = [
        { id: "#centerBtn", handler: () => centerTree(g, container.node(), zoom, baseTranslate) },
        { id: "#pngBtn", handler: () => exportPNG(svgNode) },
        { id: "#svgBtn", handler: () => exportSVG(svgNode) },
        { id: "#fullscreenBtn", handler: () => toggleFullscreen(container.node()) }
    ];

    controls.forEach(ctrl => {
        const el = document.querySelector(ctrl.id);
        if (el) {
        el.onclick = ctrl.handler;
        console.log(`✅ Contrôle attaché : ${ctrl.id}`);
        } else {
        console.warn(`⚠️ Contrôle introuvable : ${ctrl.id}`);
        }
    });

    // ✅ Recherche : Enter & Click
    const searchInput = document.getElementById("treeSearch");
    const searchBtn = document.getElementById("searchBtn");

    if (searchInput) {
        searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            searchHandler.executeSearch(searchInput.value);
        }
        });
        console.log("✅ Listener Enter attaché");
    } else {
        console.warn("⚠️ Champ #treeSearch introuvable.");
    }

    if (searchBtn) {
        searchBtn.addEventListener("click", () => {
        searchHandler.executeSearch(searchInput?.value || "");
        });
        console.log("✅ Bouton recherche attaché");
    } else {
        console.warn("⚠️ Bouton #searchBtn introuvable.");
    }

    // ✅ Si update() fourni → appliquer au Mise à jour de l'arbre au chargement
    if (typeof update === "function") {
        console.log("⏳ Appel update(root) au chargement");
        update(root);
    }

    // ✅ Zoom init + centrage
    initializeZoom(svgRoot, container.node(), zoom, baseTranslate);
    }
}
/**
 * Initialise le zoom D3 et recentre une fois.
 */
export function initializeZoom(svgRoot, containerEl, zoom, baseTranslate) {
  console.log("⚙️ initializeZoom() → containerEl :", containerEl);
  console.log("⚙️ initializeZoom() → baseTranslate :", baseTranslate);

  try {
    if (!zoom) {
      console.error("❌ initializeZoom : zoom manquant");
      return;
    }

    d3.select(containerEl).call(zoom);

    setTimeout(() => {
      console.log("🗂️ Appel initial centerTree depuis initializeZoom()");
      centerTree(svgRoot, containerEl, zoom, baseTranslate);
    }, 200);

  } catch (err) {
    console.error("❌ initializeZoom() échoué :", err);
  }
/**
 * Alternative DOM (pour comparaison, optionnel).
 */
function setupDOMSearchHighlight() {
  const input = document.getElementById("tree-search");
  if (!input) return;

  input.addEventListener("input", debounce(() => {
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll("#wrapper .node").forEach(node => {
      const text = node.textContent.toLowerCase();
      node.classList.toggle("node--highlight", query && text.includes(query));
    });
  }, 300));
 }
 }
  // ✅ Rendez TOUT accessible global
window.centerTree = centerTree;
window.exportPNG = exportPNG;
window.exportSVG = exportSVG;
window.toggleFullscreen = toggleFullscreen;
window.setupTreeControls = setupTreeControls;

console.log("✅ controls.js prêt");
