// static/js/tree/core.js
export async function loadTreeData(rootId = 1) {
    const response = await fetch(`/api/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur de chargement des données");
    return processTreeData(await response.json());
}

export async function initTree(rootId = 1) {
    try {
        return await loadTreeData(rootId);
    } catch (error) {
        console.error("Erreur dans initTree:", error);
        throw error;
    }
}

export function processTreeData(data) {
    const nodes = [];
    
    function processNode(person, level = 0) {
        const node = {
            id: person.id,
            name: `${person.first_name} ${person.last_name}`,
            level: level,
            gender: person.gender,
            photo: person.photo_url || '',
            children: []
        };

        if (person.children) {
            person.children.forEach(child => {
                node.children.push(processNode(child, level + 1));
            });
        }

        return node;
    }

    if (!Array.isArray(data)) throw new Error("Format de données invalide");
    return data.map(root => processNode(root));
}
