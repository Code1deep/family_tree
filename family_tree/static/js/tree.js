// static/js/tree.js
document.addEventListener('DOMContentLoaded', function () {
    // CSS inline
    const style = document.createElement("style");
    style.textContent = `
        #tree-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        .tree-button {
            background: #444;
            color: white;
            border: none;
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 0.9rem;
        }
        .tree-button:hover {
            background: #222;
        }
        svg {
            width: 100%;
            height: auto;
        }
    `;
    document.head.appendChild(style);

    const container = document.getElementById("tree-container");
    const margin = { top: 50, right: 90, bottom: 30, left: 90 };

    // Boutons
    const controls = document.createElement("div");
    controls.id = "tree-controls";
    controls.innerHTML = `
        <button class="tree-button" id="centerBtn">Centrer</button>
        <button class="tree-button" id="exportSvgBtn">Exporter SVG</button>
        <button class="tree-button" id="exportPngBtn">Exporter PNG</button>
        <button class="tree-button" id="fullscreenBtn">Plein écran</button>
    `;
    container.before(controls);

    let svgContainer, svg, zoom;

    function initSvg() {
        d3.select("#tree-container svg").remove();
        svgContainer = d3.select("#tree-container")
            .append("svg")
            .attr("preserveAspectRatio", "xMidYMid meet")
            .attr("viewBox", `0 0 ${container.clientWidth} ${window.innerHeight * 0.8}`)
            .classed("svg-content-responsive", true);
        svg = svgContainer.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            .on("zoom", event => svg.attr("transform", event.transform));

        svgContainer.call(zoom);
    }

    function drawTree(data) {
        const width = container.clientWidth;
        const height = window.innerHeight * 0.8;

        svg.selectAll("*").remove();

        const root = d3.hierarchy(data);
        d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right])(root);

        const colorScale = d3.scaleOrdinal()
            .domain(d3.range(6))
            .range(["#6a0dad", "#1e90ff", "#32cd32", "#ff8c00", "#ff1493", "#2c3e50"]);

        svg.selectAll(".link")
            .data(root.links())
            .enter().append("path")
            .attr("class", "link")
            .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x))
            .attr("stroke", "#999")
            .attr("fill", "none");

        const node = svg.selectAll(".node")
            .data(root.descendants())
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`)
            .style("cursor", "pointer");

        node.append("circle")
            .attr("r", 0)
            .attr("fill", d => colorScale(d.depth))
            .attr("stroke", "#fff")
            .attr("stroke-width", 2)
            .transition().duration(500).attr("r", 10);

        node.append("text")
            .attr("dy", ".35em")
            .attr("x", d => d.children ? -15 : 15)
            .style("text-anchor", d => d.children ? "end" : "start")
            .text(d => `${d.data.first_name} ${d.data.last_name}`);

        node.append("title")
            .text(d => `${d.data.first_name} ${d.data.last_name}`);

        node.on("mouseover", function () {
            d3.select(this).select("circle").transition().duration(200).attr("r", 13);
        }).on("mouseout", function () {
            d3.select(this).select("circle").transition().duration(200).attr("r", 10);
        });

        node.on("click", function (event, d) {
            window.location.href = `/person/${d.data.id}`;
        });

        centerTree();
    }

    function centerTree() {
        const bounds = svg.node().getBBox();
        const fullWidth = container.clientWidth;
        const fullHeight = window.innerHeight * 0.8;
        const scale = 1;
        const translateX = (fullWidth - bounds.width) / 2 - bounds.x;
        const translateY = (fullHeight - bounds.height) / 2 - bounds.y;
        svg.transition().duration(500).attr("transform", `translate(${translateX},${translateY}) scale(${scale})`);
    }

    function fetchDataAndDrawTree() {
        fetch("/api/tree")
            .then(response => {
                if (!response.ok) throw new Error(`Erreur HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (!data || data.error) throw new Error(data.error || "Données vides");
                initSvg();
                drawTree(data);
            })
            .catch(error => {
                console.error("Erreur :", error);
                container.innerHTML = "<div>Erreur lors du chargement de l'arbre.</div>";
            });
    }

    // Export PNG
    function exportAsPNG() {
        const svgEl = document.querySelector("#tree-container svg");
        const svgData = new XMLSerializer().serializeToString(svgEl);
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const img = new Image();
        const width = svgEl.viewBox.baseVal.width;
        const height = svgEl.viewBox.baseVal.height;
        canvas.width = width;
        canvas.height = height;
        img.onload = function () {
            ctx.drawImage(img, 0, 0);
            const png = canvas.toDataURL("image/png");
            const a = document.createElement("a");
            a.href = png;
            a.download = "arbre.png";
            a.click();
        };
        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    }

    // Export SVG
    function exportAsSVG() {
        const svgEl = document.querySelector("#tree-container svg");
        const svgData = new XMLSerializer().serializeToString(svgEl);
        const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "arbre.svg";
        a.click();
        URL.revokeObjectURL(url);
    }

    // Plein écran
    function toggleFullscreen() {
        const el = document.documentElement;
        if (!document.fullscreenElement) {
            el.requestFullscreen().catch(err => console.error(err));
        } else {
            document.exitFullscreen();
        }
    }

    // Event listeners
    document.getElementById("centerBtn").addEventListener("click", centerTree);
    document.getElementById("exportPngBtn").addEventListener("click", exportAsPNG);
    document.getElementById("exportSvgBtn").addEventListener("click", exportAsSVG);
    document.getElementById("fullscreenBtn").addEventListener("click", toggleFullscreen);
    window.addEventListener("resize", fetchDataAndDrawTree);

    fetchDataAndDrawTree();
});
