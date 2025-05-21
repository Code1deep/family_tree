// static/js/tree.js
document.addEventListener('DOMContentLoaded', function () {
    const width = window.innerWidth * 0.9;
    const height = window.innerHeight * 0.8;
    const margin = { top: 50, right: 90, bottom: 30, left: 90 };

    const svgContainer = d3.select("#tree-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const svg = svgContainer.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    d3.json("/api/tree")
        .then(data => {
            if (!data || data.error) {
                throw new Error(data.error || "Données vides");
            }

            const root = d3.hierarchy(data);
            const treeLayout = d3.tree().size([
                height - margin.top - margin.bottom,
                width - margin.left - margin.right
            ]);
            treeLayout(root);

            const colorScale = d3.scaleOrdinal()
                .domain(d3.range(6))
                .range(["#6a0dad", "#1e90ff", "#32cd32", "#ff8c00", "#ff1493", "#2c3e50"]);

            // Links
            svg.selectAll(".link")
                .data(root.links())
                .enter()
                .append("path")
                .attr("class", "link")
                .attr("d", d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x))
                .attr("stroke", "#999")
                .attr("fill", "none");

            // Nodes
            const node = svg.selectAll(".node")
                .data(root.descendants())
                .enter()
                .append("g")
                .attr("class", "node")
                .attr("transform", d => `translate(${d.y},${d.x})`)
                .style("cursor", "pointer");

            node.append("circle")
                .attr("r", 10)
                .attr("fill", d => colorScale(d.depth))
                .attr("stroke", "#fff")
                .attr("stroke-width", 2);

            node.append("text")
                .attr("dy", ".35em")
                .attr("x", d => d.children ? -15 : 15)
                .style("text-anchor", d => d.children ? "end" : "start")
                .text(d => `${d.data.first_name} ${d.data.last_name}`);

            // Hover
            node.on("mouseover", function () {
                d3.select(this).select("circle")
                    .transition()
                    .duration(200)
                    .attr("r", 13);
            }).on("mouseout", function () {
                d3.select(this).select("circle")
                    .transition()
                    .duration(200)
                    .attr("r", 10);
            });

            // Click: redirection vers page personne
            node.on("click", function (event, d) {
                // 👉 Tu peux remplacer ça par showModal(d.data.id) si tu as un modal
                window.location.href = `/person/${d.data.id}`;
            });

            // Zoom & pan
            const zoom = d3.zoom()
                .scaleExtent([0.5, 2])
                .on("zoom", (event) => {
                    svg.attr("transform", event.transform);
                });

            svgContainer.call(zoom);
        })
        .catch(error => {
            console.error("Erreur de chargement de l'arbre généalogique :", error);
            d3.select("#tree-container")
                .append("div")
                .text("Erreur lors du chargement de l'arbre. Veuillez réessayer.");
        });
});
