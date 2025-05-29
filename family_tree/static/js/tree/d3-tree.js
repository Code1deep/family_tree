// static/js/tree/d3-tree.js
import { initControls } from './controls.js';
import { centerTree, exportAsPNG, exportAsSVG, toggleFullscreen } from './utils.js';

export function initD3Tree(data) {
    console.log("Rendering tree with data:", data);
    const container = document.getElementById("tree-container");
    const margin = { top: 50, right: 90, bottom: 30, left: 90 };
    
    initControls(container);
    
    let svgContainer, svg, zoom;
    
    function initSvg() {
        d3.select("#tree-container svg").remove();
        svgContainer = d3.select("#tree-container")
            .append("svg")
            .attr("preserveAspectRatio", "xMidYMid meet")
            // ✅ Correction : template string avec backticks (``)
            .attr("viewBox", `0 0 ${container.clientWidth} ${window.innerHeight * 0.8}`);
        
        svg = svgContainer.append("g")
            // ✅ Correction : template string avec backticks
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

        // ✅ Reconstruire l’arbre imbriqué
        const treeData = buildTreeFromEdges(data.nodes, data.edges);
        const root = d3.hierarchy(treeData);

        d3.tree().size([width - margin.left - margin.right, height - margin.top - margin.bottom])(root);

        // Styles et couleurs
        const colorScale = d3.scaleOrdinal()
            .domain(d3.range(6))
            .range(["#6a0dad", "#1e90ff", "#32cd32", "#ff8c00", "#ff1493", "#2c3e50"]);

        // Dessin des liens
        svg.selectAll(".link")
            .data(root.links())
            .join("path")
            .attr("class", "link")
            .attr("d", d3.linkVertical().x(d => d.x).y(d => d.y))
            .attr("stroke", "#999")
            .attr("fill", "none");

        // Dessin des nœuds
        const node = svg.selectAll(".node")
            .data(root.descendants())
            .join("g")
            .attr("class", "node")
            // ✅ Correction : template string avec backticks
            .attr("transform", d => `translate(${d.y},${d.x})`)
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

        // Interactions
        node.on("mouseover", function() {
            d3.select(this).select("circle").transition().attr("r", 13);
        }).on("mouseout", function() {
            d3.select(this).select("circle").transition().attr("r", 10);
        }).on("click", function(event, d) {
            // ✅ Correction : template string avec backticks
            window.location.href = `/person/${d.data.id}`;
        });

        centerTree(svg, container);
    }

    drawTree(data);
}
