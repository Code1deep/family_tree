// static/js/tree/utils.js
console.log("✅ utils.js chargé");

export function setupAdvancedSearch(root, svgRoot, zoom, width, height, update) {
  console.log("✅ JS de recherche chargé");
  
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const searchField = document.getElementById("searchField");
  
  console.log("searchInput =", searchInput);
  console.log("searchBtn =", searchBtn);
  console.log("searchField =", searchField);

  searchBtn.addEventListener("click", () => {
    console.log("✅ Bouton recherche cliqué !");
    const term = searchInput.value.toLowerCase().trim();
    const field = searchField.value;
  
    console.log("Terme =", term, "Field =", field);
  
    const match = root.descendants().find(d => {
      let val = "";
      if (field === "name") val = d.data.name?.toLowerCase();
      else if (field === "birth_year") val = String(d.data.birth_year || "");
      else if (field === "generation") val = String(d.depth);
      return val.includes(term);
    });
  
    console.log("Match trouvé :", match);
  
    if (match) {
      focusNode(match);
    } else {
      alert("Aucun résultat !");
    }
  });

  function focusNode(node) {
    if (node._children) {
      node.children = node._children;
      node._children = null;
    }

    // ⚡ Recalcul layout
    update(node);

    console.log("FocusNode:", node);
    console.log("node.x =", node.x, "node.y =", node.y);

    const x = node.x;
    const y = node.y;

    svgRoot.transition().duration(750).call(
      zoom.transform,
      d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1)
        .translate(-y, -x)
    );
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
