<template>
  <div class="speech-input">
    <button 
      @click="toggleRecording" 
      :class="['speech-btn', { 'recording': isRecording, 'processing': isProcessing }]"
      :disabled="isProcessing"
    >
      <div class="mic-icon">
        <svg v-if="!isRecording" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
          <line x1="12" y1="19" x2="12" y2="23"/>
          <line x1="8" y1="23" x2="16" y2="23"/>
        </svg>
        <div v-else class="recording-animation">
          <div class="wave"></div>
          <div class="wave"></div>
          <div class="wave"></div>
        </div>
      </div>
      <span class="btn-text">
        {{ isRecording ? 'Stop Recording' : isProcessing ? 'Processing...' : 'Voice Input' }}
      </span>
    </button>
    
    <div v-if="transcript" class="transcript">
      <p><strong>Recognition Result: </strong>{{ transcript }}</p>
    </div>
    
    <div v-if="error" class="error">
      <p>❌ {{ error }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpeechInput',
  props: {
    language: {
      type: String,
      default: 'zh-CN'
    }
  },
  data() {
    return {
      isRecording: false,
      isProcessing: false,
      transcript: '',
      error: '',
      recognition: null,
      mediaRecorder: null,
      audioChunks: []
    }
  },
  mounted() {
    this.initializeSpeechRecognition()
  },
  methods: {
    initializeSpeechRecognition() {
      // Check browser support
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        this.error = 'Your browser does not support speech recognition'
        return
      }

      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      this.recognition = new SpeechRecognition()
      
      this.recognition.continuous = false
      this.recognition.interimResults = false
      this.recognition.lang = this.language
      this.recognition.maxAlternatives = 1

      this.recognition.onstart = () => {
        this.isRecording = true
        this.error = ''
        this.transcript = ''
      }

      this.recognition.onresult = (event) => {
        const result = event.results[0][0].transcript
        this.transcript = result
        this.$emit('speech-result', result)
      }

      this.recognition.onerror = (event) => {
        this.error = this.getErrorMessage(event.error)
        this.isRecording = false
        this.isProcessing = false
      }

      this.recognition.onend = () => {
        this.isRecording = false
        this.isProcessing = false
      }
    },

    getErrorMessage(error) {
      const errorMessages = {
        'no-speech': 'No speech detected, please try again',
        'audio-capture': 'Cannot access microphone, please check permissions',
        'not-allowed': 'Microphone permission denied, please allow in browser settings',
        'network': 'Network error, please check your connection',
        'aborted': 'Speech recognition interrupted',
        'language-not-supported': 'Current language not supported'
      }
      return errorMessages[error] || `Speech recognition error: ${error}`
    },

    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording()
      } else {
        await this.startRecording()
      }
    },

    async startRecording() {
      try {
        this.isProcessing = true
        
        // 检查麦克风权限
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        stream.getTracks().forEach(track => track.stop())
        
        // 开始语音识别
        this.recognition.start()
      } catch (error) {
        this.error = 'Cannot access microphone, please check permissions'
        this.isProcessing = false
      }
    },

    stopRecording() {
      if (this.recognition) {
        this.recognition.stop()
      }
    },

    // 备用方案：使用录音 + 后端语音识别
    async startAudioRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        this.mediaRecorder = new MediaRecorder(stream)
        this.audioChunks = []

        this.mediaRecorder.ondataavailable = (event) => {
          this.audioChunks.push(event.data)
        }

        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' })
          await this.sendAudioToBackend(audioBlob)
        }

        this.mediaRecorder.start()
        this.isRecording = true
      } catch (error) {
        this.error = 'Cannot access microphone'
      }
    },

    async sendAudioToBackend(audioBlob) {
      try {
        this.isProcessing = true
        const formData = new FormData()
        formData.append('audio', audioBlob, 'recording.wav')

        const response = await fetch('/api/speech-to-text', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error('Speech recognition failed')
        }

        const result = await response.json()
        this.transcript = result.text
        this.$emit('speech-result', result.text)
      } catch (error) {
        this.error = 'Speech recognition failed, please try again'
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.speech-input {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.speech-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid #4CAF50;
  background: white;
  color: #4CAF50;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 140px;
  justify-content: center;
}

.speech-btn:hover:not(:disabled) {
  background: #4CAF50;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.speech-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.speech-btn.recording {
  background: #f44336;
  color: white;
  border-color: #f44336;
  animation: pulse 1.5s infinite;
}

.speech-btn.processing {
  background: #ff9800;
  color: white;
  border-color: #ff9800;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.mic-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.recording-animation {
  display: flex;
  gap: 2px;
  align-items: center;
}

.wave {
  width: 3px;
  height: 12px;
  background: currentColor;
  border-radius: 2px;
  animation: wave 1s infinite ease-in-out;
}

.wave:nth-child(2) {
  animation-delay: 0.1s;
}

.wave:nth-child(3) {
  animation-delay: 0.2s;
}

@keyframes wave {
  0%, 40%, 100% { transform: scaleY(0.4); }
  20% { transform: scaleY(1); }
}

.transcript {
  background: #f5f5f5;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
  max-width: 300px;
  word-wrap: break-word;
}

.transcript p {
  margin: 0;
  color: #333;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 8px 12px;
  border-radius: 6px;
  border-left: 4px solid #f44336;
  max-width: 300px;
  text-align: center;
}

.error p {
  margin: 0;
  font-size: 14px;
}
</style>
