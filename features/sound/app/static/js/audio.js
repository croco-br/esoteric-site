// Shared audio-player + fetch helpers with client-side blob caching.

const audioPlayer = document.getElementById("audio-player");

const urlCache = new Map();

export function stopAudio() {
    if (audioPlayer) {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
    }
}

async function fetchAudioUrl(noteName) {
    if (urlCache.has(noteName)) {
        return urlCache.get(noteName);
    }

    const response = await fetch(`/sound/audio/${encodeURIComponent(noteName)}`);
    if (!response.ok) {
        throw new Error(`Audio not found: ${response.status}`);
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    urlCache.set(noteName, audioUrl);
    return audioUrl;
}

function playAudio(audioUrl) {
    audioPlayer.src = audioUrl;
    audioPlayer.loop = true;
    audioPlayer.controls = true;
    return audioPlayer.play();
}

export async function generateAndPlay(noteName) {
    stopAudio();
    const audioUrl = await fetchAudioUrl(noteName);
    await playAudio(audioUrl);
}
