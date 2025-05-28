// static/js/tree/core.js
export async function initTree() {
    const response = await fetch("/api/visualize/tree/1");
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    return processTreeData(data);
}

function processTreeData(data) {
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

    if (!Array.isArray(data)) throw new Error("Invalid data format");
    return data.map(root => processNode(root));
}
