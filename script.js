document.addEventListener("DOMContentLoaded", () => {
    const recordBtn = document.getElementById("record-btn");
    const uploadBtn = document.getElementById("upload-btn");
    const audioUpload = document.getElementById("audio-upload");
    const outputText = document.getElementById("output-text");
    const recordingStatus = document.getElementById("recording-status");

    let mediaRecorder;
    let audioChunks = [];

    recordBtn.addEventListener("click", async () => {
        recordingStatus.innerText = "Listening...";

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append("audio", audioBlob, "recorded_audio.wav");

                try {
                    const response = await fetch("/speech-to-text", { method: "POST", body: formData });
                    const data = await response.json();
                    outputText.innerText = data.text || "No text recognized.";
                } catch (error) {
                    outputText.innerText = "Error processing speech.";
                    console.error("Error:", error);
                }

                recordingStatus.innerText = "";
            };

            audioChunks = [];
            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 5000);

        } catch (error) {
            recordingStatus.innerText = "Microphone access denied.";
            console.error("Microphone Error:", error);
        }
    });

    uploadBtn.addEventListener("click", async () => {
        const file = audioUpload.files[0];
        if (!file) {
            alert("Please select an audio file.");
            return;
        }

        const formData = new FormData();
        formData.append("audio", file);

        try {
            const response = await fetch("/speech-to-text", { method: "POST", body: formData });
            const data = await response.json();
            outputText.innerText = data.text || "No text recognized.";
        } catch (error) {
            outputText.innerText = "Error processing audio file.";
            console.error("Error:", error);
        }
    });
});
