// static/js/modal.js
export function openModal(contentHTML) {
    let modal = document.getElementById("person-modal");
    if (!modal) return;

    const content = modal.querySelector(".modal-content-body");
    content.innerHTML = contentHTML;

    modal.style.display = "block";

    // Fermer si on clique sur le fond ou le bouton
    modal.querySelector(".modal-close").onclick = () => modal.style.display = "none";
    window.onclick = e => { if (e.target === modal) modal.style.display = "none"; };
}

export function closeModal() {
    const modal = document.getElementById("custom-modal");
    if (modal) {
        modal.style.display = "none";
    }
}

