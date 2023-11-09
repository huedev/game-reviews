// Referred to MDN Web Docs for working with dialogs (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)

const searchDialog = document.querySelector("#search-modal");
const searchShowButton = document.querySelector("#search-modal-show");
const searchCloseButton = document.querySelector("#search-modal-close");
const searchDialogBackdrop = document.querySelector("#search-modal-backdrop");
const searchDialogPanel = document.querySelector("#search-modal-panel");

// Review button opens the dialog modally
if (searchShowButton) {
    searchShowButton.addEventListener("click", () => {
        showSearchDialog();
    });
}

// Cancel button closes the dialog
if (searchCloseButton) {
    searchCloseButton.addEventListener("click", () => {
        hideSearchDialog();
    });
}

function showSearchDialog() {
    searchDialog.showModal();

    // Animate dialog and backdrop to appear
    searchDialogBackdrop.classList.add("opacity-100");
    searchDialogBackdrop.classList.remove("opacity-0");
    searchDialogPanel.classList.add("opacity-100");
    searchDialogPanel.classList.remove("opacity-0");
}

function hideSearchDialog() {
    // Animate dialog and backdrop to disappear
    searchDialogBackdrop.classList.add("opacity-0");
    searchDialogBackdrop.classList.remove("opacity-100");
    searchDialogPanel.classList.add("opacity-0");
    searchDialogPanel.classList.remove("opacity-100");

    // Give animation time to finish before closing dialog
    setTimeout(function() {
        searchDialog.close();
    }, 200);
}