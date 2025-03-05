<template>
    <div style="width: 80vw;">
        <div style="display: flex; margin: 12px; justify-content: right;">
            <label for="llm"><strong>Models&nbsp;</strong></label>
            <select name="llms" id="llm" v-model="selectedModel" @change="updateURL">
                <option value="openai">OpenAI / gpt-4o</option>
                <option value="ds-r1">Deepseek / r1</option>
            </select>
        </div>
        <div class="chat-window" style="min-height: 70vh;">
            <div v-for="(message, index) in messages"   
                class="chat-message"
                :key="index" 
                :class="{ 'user': message.isUser, 'ai': !message.isUser }">
                {{ message.text }}
            </div>
        </div>
        <div style="display: flex; justify-content: space-around; margin: auto;">
            <input style="width: 75vw;" v-model="chat" placeholder="AI에게 메시지를 쓰세요" @keyup.enter="sendMessage" />
            <button @click="sendMessage">보내기</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            chat: '',
            messages: [],
            selectedModel: 'openai'
        };
    },
    created() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('model')) {
            this.selectedModel = urlParams.get('model');
        }
    },
    methods: {
        updateURL() {
            const url = new URL(window.location.href);
            url.searchParams.set('model', this.selectedModel);
            window.history.pushState({}, '', url);
        },
        async sendMessage() {
            if (!this.chat.trim()) return;

            this.messages.push({ text: this.chat, isUser: true });
            const userMessage = this.chat;
            this.chat = "";

            const API_BASE_URL = `http://${window.location.hostname}:8000`;
            const apiUrl = `${API_BASE_URL}/v1/${this.selectedModel}/stream`;

            try {
                const response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ input: userMessage })
                });

                if (!response.body) {
                    throw new Error("No response body");
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let aiResponse = "";

                this.messages.push({ text: "", isUser: false });

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    const dataMatches = chunk.match(/data: (.+)/g);
                    if (dataMatches) {
                        dataMatches.forEach((line) => {
                            try {
                                const json = JSON.parse(line.replace("data: ", "").trim());
                                if (json.content) {
                                    aiResponse += json.content;
                                    this.messages[this.messages.length - 1].text = aiResponse;
                                }
                            } catch (e) {
                                console.error("JSON Parse Error:", e);
                            }
                        });
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Something went wrong...");
            }

            this.$nextTick(() => {
                const chatWindow = document.querySelector(".chat-window");
                if (chatWindow) {
                    chatWindow.scrollTop = chatWindow.scrollHeight;
                }
            });
        }
    }
};
</script>

<style>
.chat-window {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
}

.chat-message {
    padding: 5px 10px;
    margin: 5px 0;
    border-radius: 5px;
    max-width: 70%;
}

.user {
    background-color: #d1e7ff;
    align-self: flex-end;
    text-align: right;
}

.ai {
    background-color: #f1f1f1;
    align-self: flex-start;
    text-align: left;
}
</style>