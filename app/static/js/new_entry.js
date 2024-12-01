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
        await startRecording();
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
        mediaRecorder.stop();
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
        audioPlayback.src = URL.createObjectURL(audioBlob);
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
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to save entry.');
            }
            return response.json();
        })
        .then(data => {
            // Redirect to the new note entry using the note_id returned from the response
            window.location.href = `/view_entry/${data.note_id}`;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save entry.');
        });
    }
});

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0) {
            // Send each chunk as it becomes available
            audioChunks.push(event.data);
            await streamAudioChunk(event.data);
        }
    };

    mediaRecorder.start(2000); // Request data every 2000 ms (2 second)
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
    }, 2000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

async function streamAudioChunk(audioData) {
    const formData = new FormData();
    formData.append('audio', audioData);

    try {
        const response = await fetch('/new_entry/stream_audio', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            updateLiveTranscription(data.transcription);
        }
    } catch (error) {
        console.error('Error streaming audio chunk:', error);
    }
}

function updateProgressBar(seconds) {
    const maxTime = 120; // e.g., 2 minutes maximum
    const percentage = Math.min((seconds / maxTime) * 100, 100);
    document.getElementById('recording-progress').style.width = percentage + '%';
}

function updateLiveTranscription(text) {
    liveTranscript += ' ' + text;
    const transcriptWords = liveTranscript.split(' ');
    const maxWordsPerLine = 10;
    liveTranscription.textContent = transcriptWords.slice(-20 * maxWordsPerLine).join(' ');

    // Auto-scroll the transcription box to the bottom
    liveTranscription.scrollTop = liveTranscription.scrollHeight;
}
