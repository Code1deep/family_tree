// static/js/tree/utils.js
console.log("✅ utils.js chargé");

export function setupAdvancedSearch(root, svgRoot, zoom, width, height, update, tree) {
  console.log("✅ JS de recherche chargé");

  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const searchField = document.getElementById("searchField");
  const resultsDiv = document.getElementById("searchResults");

  console.log("searchInput =", searchInput);
  console.log("searchBtn =", searchBtn);
  console.log("searchField =", searchField);

  searchBtn.addEventListener("click", () => {
    console.log("✅ Bouton recherche cliqué !");
    const term = searchInput.value.toLowerCase().trim();
    const field = searchField.value;

    console.log("Terme =", term, "Field =", field);
    
  const termNorm = normalizeArabic(term);
  
  const matches = root.descendants().filter(d => {
    let val = "";
    if (field === "name") val = normalizeArabic(d.data.name || "");
    else if (field === "birth_year") val = String(d.data.birth_year || "");
    else if (field === "generation") val = String(d.depth);
    return val.includes(termNorm);
  });

    console.log("Matches trouvés :", matches);

    resultsDiv.innerHTML = ""; // Vider avant de remplir

    if (matches.length > 0) {
      matches.forEach(node => {
        const btn = document.createElement("button");
        btn.className = "list-group-item list-group-item-action";
        btn.innerText = `${node.data.name} (Génération ${node.depth})`;

        btn.addEventListener("click", () => {
          update(root);
          focusNode(node);
          drawArrow(node);
        });

        resultsDiv.appendChild(btn);
      });
    } else {
      resultsDiv.innerHTML = "<div class='text-danger'>Aucun résultat !</div>";
    }
  });

  function focusNode(node) {
  if (node._children) {
    node.children = node._children;
    node._children = null;
  }

  tree(root); // Re-layout
  update(root); // Redessiner
    
  console.log("FocusNode mis à jour:", node);
  console.log("updated.x =", node.x, "updated.y =", node.y);

  // Centrage propre :
  const x = node.x;
  const y = node.y;

  const scale = 1; // Optionnel : ajuster si ton arbre est très grand

  svgRoot.transition().duration(750).call(
    zoom.transform,
    d3.zoomIdentity
      .translate(width / 2, height / 2)
      .scale(scale)
      .translate(-y, -x)
  );
}

  function normalizeArabic(text) {
    return text
      .replace(/[\u064B-\u0652]/g, "") // Enlève toutes les harakat
      .replace(/[إأآ]/g, "ا")           // Normalise les alef
      .replace(/ة/g, "ه")               // Optionnel : normalise ta marbouta -> ha
      .replace(/ى/g, "ي")               // Alef Maqsura -> Ya
      .trim();
  }

  function drawArrow(node) {
    svgRoot.selectAll("line.search-arrow").remove();

    // Définir la flèche une seule fois si besoin :
    if (svgRoot.select("defs").empty()) {
      const defs = svgRoot.append("defs");
      defs.append("marker")
        .attr("id", "arrow")
        .attr("viewBox", [ -width/2, -height/2, width, height ]);
        .overflow: visible;
        .attr("refX", 10)
        .attr("refY", 0)
        .attr("markerWidth", 4)
        .attr("markerHeight", 4)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "red");
    }

    svgRoot.append("line")
      .attr("class", "search-arrow")
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", -node.y)
      .attr("y2", node.x)
      .attr("stroke", "red")
      .attr("stroke-width", 2)
      .attr("marker-end", "url(#arrow)");
  }
}

/* Debounce générique */
export function debounce(func, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

/* Throttle générique */
export function throttle(func, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/* Téléchargement basique */
export function downloadURL(dataUrl, filename) {
  const a = document.createElement("a");
  a.href = dataUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

/* Export PNG à partir d'un container ID */
export function exportAsPNG(containerId) {
  console.log("✅ exportAsPNG exécuté");
  const svgNode = document.querySelector(`#${containerId} svg`);
  if (!svgNode) {
    console.error("❌ SVG introuvable pour exportAsPNG");
    return;
  }

  const serializer = new XMLSerializer();
  const svgString = serializer.serializeToString(svgNode);

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

    const offsetX = (canvas.width - img.width) / 4;
    const offsetY = (canvas.height - img.height) / 2;

    ctx.drawImage(img, offsetX, offsetY);
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
/* Export PNG à partir d'un node SVG direct */
export function exportPNG(svgNode) {
  console.log("✅ exportPNG exécuté");
  if (!svgNode) {
    console.error("❌ Aucun SVG passé à exportPNG");
    return;
  }

  const svgData = new XMLSerializer().serializeToString(svgNode);
  const bbox = svgNode.getBBox();

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = bbox.width + 40;
  canvas.height = bbox.height + 40;

  const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(svgBlob);

  const img = new Image();
  img.onload = function () {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 20, 20);
    URL.revokeObjectURL(url);

    const png = canvas.toDataURL("image/png");
    downloadURL(png, "tree.png");
  };
  img.onerror = function (e) {
    console.error("❌ Erreur chargement image SVG :", e);
    URL.revokeObjectURL(url);
  };

  img.src = url;
}

/* Export SVG brut */
export function exportSVG(svgNode) {
  console.log("✅ exportSVG exécuté");
  if (!svgNode) {
    console.error("❌ Aucun SVG pour exportSVG");
    return;
  }
  const serializer = new XMLSerializer();
  const source = serializer.serializeToString(svgNode);
  const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  downloadURL(url, "tree.svg");
}

/* Fullscreen générique */
export function toggleFullscreen(container) {
  console.log("✅ toggleFullscreen exécuté");
  if (!document.fullscreenElement) {
    container.requestFullscreen().catch(err => {
      console.warn("⚠️ fallback vendor prefixes:", err);
      if (container.webkitRequestFullscreen) {
        container.webkitRequestFullscreen();
      } else if (container.msRequestFullscreen) {
        container.msRequestFullscreen();
      }
    });
  } else {
    document.exitFullscreen().catch(err => {
      console.error("❌ Erreur exitFullscreen :", err);
    });
  }
}

export function buildTreeFromEdges(nodes, edges) {
    console.log("✅ buildTreeFromEdges exécuté");
    const nodeMap = new Map(nodes.map(node => [node.id, { ...node, children: [] }]));
    edges.forEach(edge => {
        const parent = nodeMap.get(edge.source);
        const child = nodeMap.get(edge.target);
        if (parent && child) {
            parent.children.push(child);
        }
    });
    const childIds = new Set(edges.map(e => e.target));
    const rootNode = nodes.find(node => !childIds.has(node.id));
    if (!rootNode) {
        console.error("❌ Aucun nœud racine trouvé");
        return null;
    }
    return nodeMap.get(rootNode.id);
}

/* Centrage générique avec zoom */
export function centerTree(g, container, zoom, baseTranslate) {
  console.log("✅ centerTree exécuté");
  console.log("🔎 g =", g);
  console.log("🔎 container =", container);
  console.log("🔎 zoom =", zoom);
  console.log("🔎 baseTranslate =", baseTranslate);

  const bbox = g.node().getBBox();
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;

  const scale = Math.min(
    containerWidth / bbox.width,
    containerHeight / bbox.height,
    1
  );

  const translate = [
    (containerWidth - bbox.width * scale) / 2 - bbox.x * scale,
    (containerHeight - bbox.height * scale) / 2 - bbox.y * scale
  ];

  console.log("📐 BBox :", bbox);
  console.log("📏 Calcul scale :", scale);
  console.log("📍 Translation :", translate);

  const svgRoot = d3.select(g.node().ownerSVGElement);

  if (zoom && typeof zoom.transform === "function") {
    const finalTransform = baseTranslate
      .translate(translate[0], translate[1])
      .scale(scale);

    svgRoot.transition()
      .duration(750)
      .call(zoom.transform, finalTransform);

    console.log("✅ Transformation via zoom appliquée");
  } else {
    g.transition()
      .duration(750)
      .attr("transform", `translate(${translate[0]},${translate[1]}) scale(${scale})`);
    console.log("✅ Transformation manuelle appliquée");
  }
}

/* Recherche basique */
export function searchNode(query, svgRoot) {
  console.log("✅ searchNode exécuté :", query);
  if (!svgRoot) {
    console.warn("❌ Pas de svgRoot pour searchNode !");
    return;
  }

  const term = query.trim().toLowerCase();
  svgRoot.selectAll("g.node text")
    .style("font-weight", function () {
      return this.textContent.toLowerCase().includes(term) ? "bold" : "normal";
    })
    .style("fill", function () {
      return this.textContent.toLowerCase().includes(term) ? "red" : "black";
    });
}
window.searchNode = searchNode;
