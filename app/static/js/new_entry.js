let isRecording = false;
let isPaused = false;
let mediaRecorder;
let timerInterval;
let seconds = 0;
let audioChunks = [];
let liveTranscript = '';

const recordButton = document.getElementById('record-btn');
const pauseButton = document.getElementById('pause-btn');
const stopButton = document.getElementById('stop-btn');
const reRecordButton = document.getElementById('re-record-btn');
const playbackButton = document.getElementById('playback-btn');
const saveButton = document.getElementById('save-btn');
const audioPlayback = document.getElementById('audio-playback');
const timerDisplay = document.getElementById('timer');
const liveTranscription = document.getElementById('live-transcription');

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        // Start recording
        isRecording = true;
        recordButton.style.display = 'none';
        pauseButton.style.display = 'inline-block';
        stopButton.style.display = 'inline-block';
        reRecordButton.style.display = 'none';
        playbackButton.style.display = 'none';
        saveButton.style.display = 'none';
        audioPlayback.style.display = 'none';
        startTimer();
        startRecording();
    }
});

pauseButton.addEventListener('click', () => {
    if (isRecording) {
        if (!isPaused) {
            // Pause recording
            mediaRecorder.pause();
            isPaused = true;
            pauseButton.textContent = '▶️ Resume Recording';
            stopTimer();
        } else {
            // Resume recording
            mediaRecorder.resume();
            isPaused = false;
            pauseButton.textContent = '⏸️ Pause Recording';
            startTimer();
        }
    }
});

stopButton.addEventListener('click', () => {
    if (isRecording) {
        // Stop recording
        isRecording = false;
        stopRecording();
        stopButton.style.display = 'none';
        pauseButton.style.display = 'none';
        reRecordButton.style.display = 'inline-block';
        playbackButton.style.display = 'inline-block';
        saveButton.style.display = 'inline-block';
        stopTimer();
    }
});

reRecordButton.addEventListener('click', () => {
    resetRecording();
    reRecordButton.style.display = 'none';
    playbackButton.style.display = 'none';
    saveButton.style.display = 'none';
    audioPlayback.style.display = 'none';
    recordButton.style.display = 'inline-block';
});

playbackButton.addEventListener('click', () => {
    if (audioChunks.length > 0) {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav; codecs=MS_PCM' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;
        audioPlayback.style.display = 'block';
    }
});

saveButton.addEventListener('click', () => {
    if (audioChunks.length > 0 && liveTranscript) {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav; codecs=MS_PCM' });
        const formData = new FormData();
        formData.append('audio', audioBlob);
        formData.append('transcription', liveTranscript);

        fetch('/new_entry/save_entry', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (response.ok) {
                alert('Entry saved successfully!');
                // Redirect to the new note entry using the note_id returned from the response
                window.location.href = `/view_entry/${data.note_id}`;
            } else {
                alert('Failed to save entry.');
            }
        })
        .catch(error => console.error('Error:', error));
    }
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
        // Once recording is stopped, allow playback
        audioChunks = [...audioChunks]; // Keep the recorded chunks for playback
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
    const transcriptWords = liveTranscript.split(' ');
    const maxWordsPerLine = 10;
    const displayedTranscript = transcriptWords.slice(-2 * maxWordsPerLine).join(' ');

    liveTranscription.textContent = displayedTranscript;
    liveTranscription.scrollTop = liveTranscription.scrollHeight; // Auto-scroll
}
