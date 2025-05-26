// static/js/tree.js
import { initTree } from './tree/core.js';
import { initD3Tree } from './tree/d3-tree.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const treeData = await initTree();
        initD3Tree(treeData);
    } catch (error) {
        console.error("Tree initialization error:", error);
        alert("حدث خطأ أثناء تحميل شجرة العائلة");
    }
});
