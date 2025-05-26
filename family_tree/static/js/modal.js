// static/js/modal.js
function showModal(personId) {
    fetch(`/api/person/${personId}`)
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            document.getElementById("modalName").textContent = 
                `${data.first_name} ${data.last_name}`;
            document.getElementById("modalMother").textContent = 
                data.mother_name || "غير معروفة";
            document.getElementById("bioLink").href = 
                `/person_bio/${personId}`;
            
            const modal = document.getElementById("personModal");
            modal.style.display = "flex";
            document.body.style.overflow = "hidden";
        })
        .catch(error => {
            console.error("Error fetching person data:", error);
            alert("حدث خطأ أثناء تحميل بيانات الشخص");
        });
}

function closeModal() {
    const modal = document.getElementById("personModal");
    modal.style.display = "none";
    document.body.style.overflow = "auto";
}

// Fermer la modale en cliquant à l'extérieur
document.getElementById("personModal").addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});
