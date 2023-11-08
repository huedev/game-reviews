// Referred to MDN Web Docs for working with dialogs (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)

const dialog = document.querySelector("#modal");
const showButton = document.querySelector("#modal-show");
const closeButton = document.querySelector("#modal-close");
const dialogBackdrop = document.querySelector("#modal-backdrop");
const dialogPanel = document.querySelector("#modal-panel");

// Review button opens the dialog modally
if (showButton) {
    showButton.addEventListener("click", () => {
        showDialog();
    });
}

// Cancel button closes the dialog
if (closeButton) {
    closeButton.addEventListener("click", () => {
        hideDialog();
    });
}

function showDialog() {
    dialog.showModal();

    // Animate dialog and backdrop to appear
    dialogBackdrop.classList.add("opacity-100");
    dialogBackdrop.classList.remove("opacity-0");
    dialogPanel.classList.add("opacity-100");
    dialogPanel.classList.remove("opacity-0");
}

function hideDialog() {
    // Animate dialog and backdrop to disappear
    dialogBackdrop.classList.add("opacity-0");
    dialogBackdrop.classList.remove("opacity-100");
    dialogPanel.classList.add("opacity-0");
    dialogPanel.classList.remove("opacity-100");

    // Give animation time to finish before closing dialog
    setTimeout(function() {
        dialog.close();
    }, 200);
}