// static/js/tree_modal.js
document.addEventListener('DOMContentLoaded', function() {
    fetch("/api/tree")
        .then(response => response.json())
        .then(data => {
            const treeData = processTreeData(data);
            renderFamilyTree(treeData);
        })
        .catch(error => {
            console.error("Error loading tree data:", error);
            alert("حدث خطأ أثناء تحميل شجرة العائلة");
        });

    function processTreeData(data) {
        const nodes = [];
        
        function processNode(person, level = 0) {
            nodes.push({
                id: person.id,
                name: `${person.first_name} ${person.last_name}`,
                level: level,
                mother: person.mother_name,
                birthDate: person.birth_date,
                photo: person.photo_url || ''
            });

            if (person.children) {
                person.children.forEach(child => processNode(child, level + 1));
            }
        }

        if (Array.isArray(data)) {
            data.forEach(root => processNode(root));
        }
        
        return nodes;
    }

    function renderFamilyTree(nodes) {
        // Implémentation de la visualisation de l'arbre
        console.log("Rendering tree with nodes:", nodes);
        // ... (votre code existant pour FamilyTree)
    }
});
