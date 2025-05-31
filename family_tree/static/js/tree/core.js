// static/js/tree/core.js
import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { transformDataForD3 } from './d3-tree.js';
import { centerTree } from './utils.js';

let svgGroup, svgRoot, zoomBehavior;
let currentScale = 1;
let searchTerm = '';

export function initTree(container, data) {
    container.innerHTML = ''; // Clear previous

    const margin = { top: 50, right: 200, bottom: 50, left: 200 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    svgRoot = d3.select(container)
        .append('svg')
        .attr('width', container.clientWidth)
        .attr('height', container.clientHeight)
        .style('font-family', 'Arial')
        .style('background-color', '#fff')
        .call(
            zoomBehavior = d3.zoom()
                .scaleExtent([0.05, 4])
                .on('zoom', (event) => svgGroup.attr('transform', event.transform))
        );

    svgGroup = svgRoot.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    buildTree(data);
}

function buildTree(data) {
    const root = d3.hierarchy(data, d => d.children || d._children);
    root.x0 = 0;
    root.y0 = 0;

    const treeLayout = d3.tree().nodeSize([30, 300]);

    root.children?.forEach(collapse);
    update(root);

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    function update(source) {
        const nodes = treeLayout(root).descendants();
        const links = treeLayout(root).links();
        nodes.forEach(d => d.y = d.depth * 180);

        const node = svgGroup.selectAll('g.node')
            .data(nodes, d => d.data.id);

        const nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr('transform', d => `translate(${source.y0},${source.x0})`)
            .on('click', onClick);

        nodeEnter.append('circle')
            .attr('r', 4)
            .style('fill', d => d._children ? '#555' : '#999');

        nodeEnter.append('text')
            .attr('dy', 3)
            .attr('x', d => d._children ? -10 : 10)
            .style('text-anchor', d => d._children ? 'end' : 'start')
            .style('font-size', '10px')
            .text(d => d.data.name);

        const nodeUpdate = nodeEnter.merge(node);
        nodeUpdate.transition().duration(500)
            .attr('transform', d => `translate(${d.y},${d.x})`);

        nodeUpdate.select('circle')
            .style('fill', d => d._children ? '#555' : '#999');

        const nodeExit = node.exit().transition().duration(500)
            .attr('transform', d => `translate(${source.y},${source.x})`)
            .remove();

        nodeExit.select('circle').attr('r', 0);
        nodeExit.select('text').style('fill-opacity', 0);

        const link = svgGroup.selectAll('path.link')
            .data(links, d => d.target.data.id);

        const diagonal = (s, d) => `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`;

        link.enter().insert('path', 'g')
            .attr('class', 'link')
            .attr('d', d => diagonal({ x: source.x0, y: source.y0 }, { x: source.x0, y: source.y0 }))
            .merge(link)
            .transition().duration(500)
            .attr('d', d => diagonal(d.source, d.target));

        link.exit().transition().duration(500)
            .attr('d', d => diagonal({ x: source.x, y: source.y }, { x: source.x, y: source.y }))
            .remove();

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
            const res = await fetch(`/api/person/visualize/tree/${d.data.id}`);
            if (res.ok) {
                const newData = await res.json();
                const newChildren = newData.children.map(transformDataForD3);
                d.children = newChildren.map(c => d3.hierarchy(c));
            }
        }
        update(d);
    }

    // Centrage automatique
    setTimeout(() => centerUtils(svgGroup, svgRoot.node()), 700);
}

export function zoomIn() {
    currentScale = Math.min(currentScale * 1.2, 4);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.05);
    svgRoot.transition().duration(300).call(zoomBehavior.scaleTo, currentScale);
}

export function centerTree() {
    centerUtils(svgGroup, svgRoot.node());
}

export function exportPNG(container) {
    const svgNode = container.querySelector('svg');
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

export function exportSVG(container) {
    const svg = container.querySelector("svg");
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.download = "tree.svg";
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
}

export function toggleFullscreen(el) {
    if (!document.fullscreenElement) {
        el.requestFullscreen().catch(err => console.error(err));
    } else {
        document.exitFullscreen();
    }
}

export function searchNode(query) {
    searchTerm = query.toLowerCase();
    svgGroup.selectAll("g.node").select("text")
        .style("fill", d => d.data.name.toLowerCase().includes(searchTerm) ? "red" : "black")
        .style("font-weight", d => d.data.name.toLowerCase().includes(searchTerm) ? "bold" : "normal");
}
