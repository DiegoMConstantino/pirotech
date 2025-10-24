document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("addProductModal");
    const btn = document.getElementById("addProductBtn");
    const span = document.querySelector(".close");
    const form = document.getElementById("productForm");
    const tableBody = document.querySelector("#productTable tbody");

    btn.onclick = () => modal.style.display = "flex";
    span.onclick = () => modal.style.display = "none";
    window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; };

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        const animal = document.getElementById("animal").value;
        const peso = document.getElementById("peso").value;
        const tipo = document.getElementById("tipo").value;
        const quantidade = document.getElementById("quantidade").value;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `<td>${animal}</td><td>${peso}</td><td>${tipo}</td><td>${quantidade}</td>`;
        tableBody.appendChild(newRow);

        modal.style.display = "none";
        form.reset();
    });
});
