//static/js/tree/loader.js 
import { initTree } from './core.js';

function renderPersonNode(person) {
    const container = document.createElement('div');
    container.className = 'person-node';
    const header = document.createElement('div');
    header.className = 'person-header';
    header.textContent = `${person.name} (${person.birthDate || "?"})`;
    container.appendChild(header);

    if (person.children && person.children.length > 0) {
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'children-container';
        person.children.forEach(child => {
            const childNode = renderPersonNode(child);
            childrenContainer.appendChild(childNode);
        });
        container.appendChild(childrenContainer);
    }

    return container;
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const treeData = await initTree(); // ← appelle core.js + transforme en arbre
        const treeContainer = document.getElementById('familyTree');
        treeContainer.innerHTML = '';
        treeData.forEach(root => {
            const node = renderPersonNode(root);
            treeContainer.appendChild(node);
        });
    } catch (err) {
        console.error("Erreur lors du chargement de l'arbre :", err);
    }
});
