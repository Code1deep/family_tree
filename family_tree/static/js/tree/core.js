// static/js/tree/core.js
import * as d3 from 'https://d3js.org/d3.v7.min.js';
import { transformDataForD3 } from './d3-tree.js';
import { centerTree } from './utils.js';

export function initD3Tree(containerId, data) {
    const margin = { top: 50, right: 200, bottom: 50, left: 200 };
    const width = 2000 - margin.left - margin.right;
    const height = 1200 - margin.top - margin.bottom;

    const container = d3.select(`#${containerId}`);
    container.selectAll("*").remove();  // Clear previous tree

    const svg = container.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .call(d3.zoom().scaleExtent([0.05, 4]).on("zoom", zoomed))
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const treeLayout = d3.tree().nodeSize([30, 300]); // Vertical spacing, horizontal depth

    const root = d3.hierarchy(data, d => d.children || d._children);
    root.x0 = 0;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    // Initial collapse for performance
    root.children?.forEach(collapse);
    update(root);

    function update(source) {
        const treeData = treeLayout(root);
        const nodes = treeData.descendants();
        const links = treeData.links();

        nodes.forEach(d => {
            d.y = d.depth * 180;
        });

        const node = svg.selectAll('g.node')
            .data(nodes, d => d.data.id);

        const nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", d => `translate(${source.y0},${source.x0})`)
            .on('click', onClick);

        nodeEnter.append('circle')
            .attr('r', 4)
            .style('fill', d => d._children ? "#555" : "#999");

        nodeEnter.append('text')
            .attr("dy", 3)
            .attr("x", d => d._children ? -10 : 10)
            .style("text-anchor", d => d._children ? "end" : "start")
            .text(d => d.data.name)
            .style("font-size", "10px");

        const nodeUpdate = nodeEnter.merge(node);
        nodeUpdate.transition().duration(500)
            .attr("transform", d => `translate(${d.y},${d.x})`);

        nodeUpdate.select('circle')
            .attr('r', 4)
            .style('fill', d => d._children ? "#555" : "#999");

        const nodeExit = node.exit().transition().duration(500)
            .attr("transform", d => `translate(${source.y},${source.x})`)
            .remove();

        nodeExit.select('circle').attr('r', 0);
        nodeExit.select('text').style('fill-opacity', 0);

        const link = svg.selectAll('path.link')
            .data(links, d => d.target.data.id);

        const linkEnter = link.enter().insert('path', "g")
            .attr("class", "link")
            .attr('d', d => {
                const o = { x: source.x0, y: source.y0 };
                return diagonal(o, o);
            });

        linkEnter.merge(link)
            .transition().duration(500)
            .attr('d', d => diagonal(d.source, d.target));

        link.exit().transition().duration(500)
            .attr('d', d => {
                const o = { x: source.x, y: source.y };
                return diagonal(o, o);
            }).remove();

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
            const response = await fetch(`/api/person/visualize/tree/${d.data.id}`);
            if (response.ok) {
                const newData = await response.json();
                const newChildren = newData.children.map(transformDataForD3);
                d.children = newChildren.map(c => d3.hierarchy(c));
            } else {
                console.error("Failed to load children dynamically");
            }
        }
        update(d);
    }

    function zoomed(event) {
        svg.attr("transform", event.transform);
    }

    // Auto-center after render
    setTimeout(() => {
        const svgNode = container.select("svg").node();
        centerTree(d3.select(svgNode).select("g"), svgNode.parentElement);
    }, 700);
}
