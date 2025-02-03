<template>
    <div>
        <div class="chat-window">
            <div v-for="(message, index) in messages" :key="index" 
                class="chat-message" :class="{'user': message.isUser, 'ai': !message.isUser}">
                {{ message.text }}
            </div>
        </div>
        <input v-model="chat" placeholder="AI에게 메시지를 쓰세요" @keyup.enter="sendMessage" />
        <button @click="sendMessage">보내기</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            chat: '',
            messages: []
        };
    },
    methods: {
        async sendMessage() {
            if (!this.chat.trim()) return;
            
            this.messages.push({ text: this.chat, isUser: true });
            const userMessage = this.chat;
            this.chat = "";
            
            try {
                const response = await fetch("http://localhost:8000/v1/openai/stream", {
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
}
.user {
    background-color: #d1e7ff;
    align-self: flex-end;
}
.ai {
    background-color: #f1f1f1;
    align-self: flex-start;
}
</style>
