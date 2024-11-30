// app/static/js/new_entry.js

let isRecording = false;
let mediaRecorder;
let timerInterval;
let seconds = 0;
let liveTranscript = '';
let audioChunks = [];

const recordButton = document.getElementById('record-btn');
const timerDisplay = document.getElementById('timer');
const reRecordButton = document.getElementById('re-record-btn');
const liveTranscription = document.getElementById('live-transcription');

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        // Start recording
        isRecording = true;
        recordButton.textContent = '⏹️ Stop';
        reRecordButton.style.display = 'none';
        startTimer();
        startRecording();
    } else {
        // Stop recording
        isRecording = false;
        recordButton.textContent = '🎙️ Record';
        reRecordButton.style.display = 'inline-block';
        stopTimer();
        stopRecording();
    }
});

reRecordButton.addEventListener('click', () => {
    resetRecording();
});

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
        streamAudio(event.data); // Stream audio chunk to server
    };

    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        audioChunks = []; // Clear the audio chunks after stopping
    };
}

function resetRecording() {
    liveTranscript = '';
    liveTranscription.textContent = 'Live transcription will appear here...';
    timerDisplay.textContent = '00:00';
    seconds = 0;
    audioChunks = [];
}

function startTimer() {
    timerInterval = setInterval(() => {
        seconds++;
        const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${minutes}:${secs}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

async function streamAudio(audioData) {
    // Simulate streaming audio to server (this would be a WebSocket or HTTP request)
    const formData = new FormData();
    formData.append('audio', audioData);

    const response = await fetch('/new_entry/stream_audio', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        updateLiveTranscription(data.transcription);
    }
}

function updateLiveTranscription(text) {
    liveTranscript += ' ' + text;
    const transcriptLines = liveTranscript.split(' ');
    const maxWordsPerLine = 10;
    const displayedTranscript = transcriptLines.slice(-2 * maxWordsPerLine).join(' ');

    liveTranscription.textContent = displayedTranscript;
}