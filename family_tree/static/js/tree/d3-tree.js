// static/js/tree/d3-tree.js
import { initControls } from './controls.js';
import { centerTree, buildTreeFromEdges, exportAsPNG, exportAsSVG, toggleFullscreen } from './utils.js';

export function initD3Tree(data) {
    console.log("Rendering tree with data:", data);
    const container = document.getElementById("tree-container");
    const margin = { top: 50, right: 90, bottom: 30, left: 90 };
    
    initControls(container);
    
    let svgContainer, svg, zoom;

    function initSvg() {
        d3.select("#tree-container svg").remove();

        const width = container.clientWidth;
        const height = window.innerHeight * 0.8;

        svgContainer = d3.select("#tree-container")
            .append("svg")
            .attr("preserveAspectRatio", "xMidYMid meet")
            .attr("viewBox", `0 0 ${width} ${height}`);

        svg = svgContainer.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            .on("zoom", event => svg.attr("transform", event.transform));

        svgContainer.call(zoom);
    }

    function drawTree(data) {
        initSvg();

        const width = container.clientWidth;
        const height = window.innerHeight * 0.8;

        const treeData = buildTreeFromEdges(data.nodes, data.edges);
        const root = d3.hierarchy(treeData);

        // ✅ Orientation verticale : x → horizontal, y → vertical
        d3.tree().size([width - margin.left - margin.right, height - margin.top - margin.bottom])(root);

        const colorScale = d3.scaleOrdinal()
            .domain(d3.range(6))
            .range(["#6a0dad", "#1e90ff", "#32cd32", "#ff8c00", "#ff1493", "#2c3e50"]);

        // ✅ Lien vertical (top-down)
        svg.selectAll(".link")
            .data(root.links())
            .join("path")
            .attr("class", "link")
            .attr("d", d3.linkVertical().x(d => d.x).y(d => d.y))
            .attr("stroke", "#999")
            .attr("stroke-width", 2)
            .attr("fill", "none");

        const node = svg.selectAll(".node")
            .data(root.descendants())
            .join("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.x},${d.y})`)
            .style("cursor", "pointer");

        node.append("circle")
            .attr("r", 0)
            .attr("fill", d => colorScale(d.depth))
            .transition().duration(500).attr("r", 10);

        node.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -15 : 15)
            .style("text-anchor", d => d.children ? "end" : "start")
            .text(d => d.data.name);

        node.on("mouseover", function() {
            d3.select(this).select("circle").transition().attr("r", 13);
        }).on("mouseout", function() {
            d3.select(this).select("circle").transition().attr("r", 10);
        }).on("click", function(event, d) {
            window.location.href = `/person/${d.data.id}`;
        });

        centerTree(svg, container);
    }

    drawTree(data);
}
