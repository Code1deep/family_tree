// static/js/tree/utils.js
export function centerTree(svg, container) {
    const bounds = svg.node().getBBox();
    const fullWidth = container.clientWidth;
    const fullHeight = window.innerHeight * 0.8;
    const translateX = (fullWidth - bounds.width) / 2 - bounds.x;
    const translateY = (fullHeight - bounds.height) / 2 - bounds.y;
    svg.transition().duration(500).attr("transform", `translate(${translateX},${translateY})`);
}

export function exportAsPNG() {
    const svgEl = document.querySelector("#tree-container svg");
    const svgData = new XMLSerializer().serializeToString(svgEl);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();
    
    canvas.width = svgEl.viewBox.baseVal.width;
    canvas.height = svgEl.viewBox.baseVal.height;
    
    img.onload = function() {
        ctx.drawImage(img, 0, 0);
        const png = canvas.toDataURL("image/png");
        downloadFile(png, "arbre.png");
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
}

export function exportAsSVG() {
    const svgEl = document.querySelector("#tree-container svg");
    const svgData = new XMLSerializer().serializeToString(svgEl);
    const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    downloadFile(url, "arbre.svg");
    URL.revokeObjectURL(url);
}

export function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(console.error);
    } else {
        document.exitFullscreen();
    }
}

function downloadFile(url, filename) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
}

export function buildTreeFromEdges(nodes, edges) {
    // Dictionnaire des nœuds par ID
    const nodeMap = new Map(nodes.map(node => [node.id, { ...node, children: [] }]));

    // Créer les relations parent → enfant
    edges.forEach(edge => {
        const parent = nodeMap.get(edge.source);
        const child = nodeMap.get(edge.target);
        if (parent && child) {
            parent.children.push(child);
        }
    });

    // Identifier la racine (nœud qui n’est enfant de personne)
    const childIds = new Set(edges.map(e => e.target));
    const rootNode = nodes.find(node => !childIds.has(node.id));

    return nodeMap.get(rootNode.id);
}
