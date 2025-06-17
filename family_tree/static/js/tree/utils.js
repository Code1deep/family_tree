// static/js/tree/utils.js
console.log("✅ utils.js chargé");

export function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

export function downloadURL(dataUrl, filename) {
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

export function exportAsPNG(containerId) {
    const svgNode = document.querySelector(`#${containerId} svg`);
    if (!svgNode) {
        console.error("❌ SVG introuvable pour export As PNG");
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

        // Centrage calculé
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

export function exportPNG(svgNode) {
    console.log("✅ exportPNG exécuté");
    if (!svgNode) {
        console.error("❌ SVG introuvable pour export PNG");
        return;
    }

    const svgData = new XMLSerializer().serializeToString(svgNode);
    const img = new Image();
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    const bbox = svgNode.getBBox();
    canvas.width = bbox.width + 40;
    canvas.height = bbox.height + 40;

    const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(svgBlob);

    img.onload = function () {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 20, 20);
        URL.revokeObjectURL(url);
        const png = canvas.toDataURL("image/png");
        downloadURL(png, "tree.png");
    };

    img.onerror = function (e) {
        console.error("❌ Erreur chargement image SVG", e);
    };

    img.src = url;
}

export function toggleFullscreen(container) {
    if (!document.fullscreenElement) {
        container.requestFullscreen().catch(err => console.error("❌ Fullscreen:", err));
    } else {
        document.exitFullscreen();
    }
}

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

export function exportSVG(svgNode) {
    console.log("✅ exportSVG exécuté");
    if (!svgNode) {
        console.error("❌ SVG introuvable pour SVG export");
        return;
    }
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svgNode);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadURL(url, "tree.svg");
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

export function centerTree(g, container, zoom) {
    console.log("✅ centerTree exécuté");
    console.log("🔎 g =", g);
    console.log("🔎 container =", container);
    console.log("🔎 zoom =", zoom);

    if (!g || typeof g.node !== "function" || !g.node()) {
        console.error("❌ g invalide dans centerTree");
        return;
    }

    const bbox = g.node().getBBox();
    if (!bbox || isNaN(bbox.width) || isNaN(bbox.height)) {
        console.error("❌ BBox invalide ou introuvable");
        return;
    }

    const scale = Math.min(
        container.clientWidth / bbox.width,
        container.clientHeight / bbox.height,
        1
    );
    const translate = [
        (container.clientWidth - bbox.width * scale) / 2 - bbox.x * scale,
        (container.clientHeight - bbox.height * scale) / 2 - bbox.y * scale
    ];

    d3.select(g.node().ownerSVGElement)
        .transition().duration(750)
        .call(zoom.transform, d3.zoomIdentity.translate(...translate).scale(scale));
}

export function searchNode(query, svgRoot) {
    console.log("✅ searchNode exécuté");
    const term = query.trim().toLowerCase();
    svgRoot.selectAll("g.node text")
        .style("font-weight", d => d.data.name.toLowerCase().includes(term) ? "bold" : "normal")
        .style("fill", d => d.data.name.toLowerCase().includes(term) ? "red" : "black");
}
