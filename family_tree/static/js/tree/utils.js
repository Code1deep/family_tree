// static/js/tree/utils.js
console.log("✅ utils.js chargé");

export function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
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

function downloadURL(dataUrl, filename) {
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

export function exportPNG(svgElementOrContainer) {
    console.log("✅ exportPNG exécuté");
    const svgNode = svgElementOrContainer.tagName === 'svg'
        ? svgElementOrContainer
        : svgElementOrContainer.querySelector('svg');

    if (!svgNode) {
        console.error("❌ SVG introuvable pour PNG");
        return;
    }

    const svgData = new XMLSerializer().serializeToString(svgNode);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    canvas.width = svgNode.clientWidth * 2;
    canvas.height = svgNode.clientHeight * 2;
    ctx.scale(2, 2);

    img.onload = () => {
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        const pngUrl = canvas.toDataURL("image/png");
        downloadURL(pngUrl, "tree.png");
    };
    img.src = url;
}

export function exportSVG(svgNode) {
    console.log("✅ exportSVG exécuté");
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svgNode);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadURL(url, "tree.svg");
}

export function toggleFullscreen(container) {
    console.log("✅ toggleFullscreen exécuté");
    if (!document.fullscreenElement) {
        container.requestFullscreen();
    } else {
        document.exitFullscreen();
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
    return nodeMap.get(rootNode.id);
}

// ✅ zoomBehavior DOIT ÊTRE PASSÉ en paramètre
export function centerTree(svgGroup, wrapper, zoomBehavior) {
    const bounds = svgGroup.node().getBBox();
    const scale = Math.min(
        wrapper.clientWidth / bounds.width,
        wrapper.clientHeight / bounds.height,
        1
    );
    const translate = [
        (wrapper.clientWidth - bounds.width * scale) / 2 - bounds.x * scale,
        (wrapper.clientHeight - bounds.height * scale) / 2 - bounds.y * scale
    ];
    d3.select(svgGroup.node().ownerSVGElement)
        .transition().duration(750)
        .call(zoomBehavior.transform, d3.zoomIdentity.translate(...translate).scale(scale));
}

export function searchNode(query, svgRoot) {
    const term = query.trim().toLowerCase();
    svgRoot.selectAll("g.node text")
        .style("font-weight", d => d.data.name.toLowerCase().includes(term) ? "bold" : "normal")
        .style("fill", d => d.data.name.toLowerCase().includes(term) ? "red" : "black");
}
