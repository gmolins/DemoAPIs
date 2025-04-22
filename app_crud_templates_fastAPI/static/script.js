console.log("Hello, World!");

document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript cargado correctamente.");

    const items = document.querySelectorAll("li a");
    items.forEach(item => {
        item.addEventListener("click", (event) => {
            alert(`Has seleccionado el item: ${item.textContent}`);
        });
    });
});

console.log("Terminado!")