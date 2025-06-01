// static/js/modal.js

export function openModal(content) {
    let modal = document.getElementById("custom-modal");
    let modalContent = document.getElementById("custom-modal-content");

    if (!modal) {
        modal = document.createElement("div");
        modal.id = "custom-modal";
        modal.style.cssText = `
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex; align-items: center; justify-content: center;
            z-index: 9999;
        `;

        modalContent = document.createElement("div");
        modalContent.id = "custom-modal-content";
        modalContent.style.cssText = `
            background: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            position: relative;
        `;

        const closeButton = document.createElement("span");
        closeButton.innerHTML = "&times;";
        closeButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 24px;
            cursor: pointer;
        `;
        closeButton.onclick = closeModal;

        modalContent.appendChild(closeButton);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
    }

    modalContent.innerHTML += `<div>${content}</div>`;
    modal.style.display = "flex";
}

export function closeModal() {
    const modal = document.getElementById("custom-modal");
    if (modal) {
        modal.style.display = "none";
    }
}
