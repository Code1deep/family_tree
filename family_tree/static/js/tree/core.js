// static/js/tree/core.js
export async function loadTreeData(rootId = 1) {
    const response = await fetch(`/api/person/visualize/tree/${rootId}`);
    if (!response.ok) throw new Error("Erreur de chargement des données");
    const jsonData = await response.json();
    console.log("Données reçues:", jsonData); 
    return processTreeData(jsonData);
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
    const idToNodeMap = {};
    const childrenMap = {};

    // Étape 1 : Construire les noeuds de base
    data.nodes.forEach(person => {
        idToNodeMap[person.id] = {
            id: person.id,
            name: person.name,
            birthDate: "", // pas fourni
            gender: "",    // pas fourni
            photo: person.photo || '',
            children: []
        };
    });

    // Étape 2 : Lier les enfants aux parents
    data.edges.forEach(edge => {
        if (edge.type === "father" || edge.type === "mother") {
            const parent = idToNodeMap[edge.from];
            const child = idToNodeMap[edge.to];
            if (parent && child) {
                parent.children.push(child);
            }
        }
    });

    // Étape 3 : Trouver les racines (nœuds sans parents)
    const childrenIds = new Set(data.edges.map(e => e.to));
    const rootNodes = Object.values(idToNodeMap).filter(node => !childrenIds.has(node.id));

    return rootNodes;
}
