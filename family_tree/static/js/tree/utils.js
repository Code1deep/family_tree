// static/js/tree/utils.js
console.log("✅ utils.js chargé");
export function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

export function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

export function exportTreeAsSVG(containerId) {
    console.log("✅ exportAsSVG exécuté");
    const svg = document.querySelector("#tree-container svg");
    if (!svg) {
        console.error("❌ SVG introuvable pour l’export");
        return;
    }
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadURL(url, "tree-visualization.svg");
}

export function exportTreeAsPNG(svgElementOrContainer) {
    console.log("✅ exportAsPNG exécuté");
    // Accepter soit <svg>, soit un conteneur contenant <svg>
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
        const link = document.createElement("a");
        link.download = "tree.png";
        link.href = pngUrl;
        link.click();
    };
    img.src = url;
}

function downloadURL(dataUrl, filename) {
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

export function centerTree(svg, container, offsetY = 50) {
    console.log("✅ centerTree exécuté");
    // centrage automatique de l’arbre
    const bbox = svg.node().getBBox();
    const x = bbox.x + bbox.width / 2;
    const y = bbox.y;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    const dx = containerWidth / 2 - x;
    const dy = offsetY - y;

    svg.transition().duration(500)
        .attr("transform", `translate(${dx},${dy})`);
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
