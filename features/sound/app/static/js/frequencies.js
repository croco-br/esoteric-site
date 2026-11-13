import { generateAndPlay, stopAudio } from './audio.js';

const btn = document.getElementById("loading-button");
const select = document.getElementById("frequency-select");

btn.addEventListener("click", generateAudio);

async function generateAudio() {
    stopAudio();
    setButtonState("loading");
    btn.disabled = true;

    try {
        await generateAndPlay(select.value);
        setButtonState("success");
    } catch (error) {
        console.error("Audio generation failed:", error);
        setButtonState("error");
    } finally {
        btn.disabled = false;
        // Return to the default label shortly after success/error feedback.
        setTimeout(() => setButtonState("default"), 2000);
    }
}

function setButtonState(state) {
    btn.dataset.state = state;
    btn.classList.remove("is-loading", "is-success", "is-error");

    const labels = {
        default: "Gerar",
        loading: "Gerando…",
        success: "Tocando ✓",
        error: "Falhou — tente novamente",
    };

    btn.textContent = labels[state];

    if (state === "loading") {
        btn.classList.add("is-loading");
    } else if (state === "success") {
        btn.classList.add("is-success");
    } else if (state === "error") {
        btn.classList.add("is-error");
    }
}
