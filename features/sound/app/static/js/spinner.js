export const spinner = document.getElementById("spinner");

export function showSpinner() {
    if (spinner) {
        spinner.hidden = false;
    }
}

export function hideSpinner() {
    if (spinner) {
        spinner.hidden = true;
    }
}
