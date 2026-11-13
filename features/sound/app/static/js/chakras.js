import { generateAndPlay } from './audio.js';
import { hideSpinner, showSpinner } from './spinner.js';

const chips = document.querySelectorAll('.chakra-chip');

// Wire image map areas (kept for the illustration) and quick-pick chips.
document.querySelectorAll('area[data-note]').forEach((area) => {
    area.addEventListener('click', (event) => {
        event.preventDefault();
        triggerGenerate(area.dataset.note);
    });
});

chips.forEach((chip) => {
    chip.addEventListener('click', () => triggerGenerate(chip.dataset.note));
});

async function triggerGenerate(name) {
    showSpinner();
    setChipsDisabled(true);

    try {
        await generateAndPlay(name);
        setActiveChip(name);
    } catch (error) {
        console.error('Audio generation failed:', error);
    } finally {
        hideSpinner();
        setChipsDisabled(false);
    }
}

function setChipsDisabled(disabled) {
    chips.forEach((chip) => {
        chip.disabled = disabled;
    });
}

function setActiveChip(name) {
    chips.forEach((chip) => {
        chip.classList.toggle('is-playing', chip.dataset.note === name);
    });
}
