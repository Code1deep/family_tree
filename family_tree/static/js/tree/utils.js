// static/js/tree/utils.js
export function centerTree(svg, container) {
    // centrage automatique de l’arbre
    const bbox = svg.node().getBBox();
    const x = bbox.x + bbox.width / 2;
    const y = bbox.y;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    const dx = containerWidth / 2 - x;
    const dy = 50 - y;

    svg.transition().duration(500)
        .attr("transform", `translate(${dx},${dy})`);
}

export function toggleFullscreen(container) {
    if (!document.fullscreenElement) {
        container.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

export function exportAsPNG(containerId) {
    console.warn("TODO: implémenter export PNG");
}

export function exportAsSVG(containerId) {
    console.warn("TODO: implémenter export SVG");
}

export function buildTreeFromEdges(nodes, edges) {
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
