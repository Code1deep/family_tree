// static/js/tree.js
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch("/api/visualize/tree/1");
        if (!response.ok) throw new Error("Network response was not ok");
        const rawData = await response.json();
        
        const treeData = processTreeData(rawData);
        initD3Tree(treeData); // Utilisation de D3.js pour le rendu
        
    } catch (error) {
        console.error("Erreur d'initialisation de l'arbre :", error);
        alert("حدث خطأ أثناء تحميل شجرة العائلة");
    }
});

function processTreeData(data) {
    // Votre logique existante de core.js
    const nodes = [];
    
    function processNode(person, level = 0) {
        nodes.push({
            id: person.id,
            name: `${person.first_name} ${person.last_name}`,
            level: level,
            mother: person.mother_name,
            birthDate: person.birth_date,
            photo: person.photo_url || '',
            children: []
        });

        if (person.children) {
            person.children.forEach(child => {
                const childNode = processNode(child, level + 1);
                nodes[nodes.length - 1].children.push(childNode);
            });
        }

        return nodes[nodes.length - 1];
    }

    if (!Array.isArray(data)) throw new Error("Format de données invalide");
    return data.map(root => processNode(root));
}
