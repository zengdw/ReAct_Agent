<script setup lang="ts">
import { ref } from 'vue';
import { VueMarkdownIt } from 'vue-markdown-shiki'

const question = ref('');
const isLoading = ref(false);
const res_text = ref('');
let thread_id = ''


// SSE 连接函数
const connectSSE = async () => {
  if (!question.value.trim()) {
    return;
  }

  isLoading.value = true;

  try {
    const url = `http://127.0.0.1:8080/sse`;

    // 使用 fetch 发送 POST 请求获取 SSE 流
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'thread_id': thread_id
      },
      body: JSON.stringify({
        question: question.value
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 获取 header 中的 thread_id
    const threadIdHeader = response.headers.get('thread_id');
    if (threadIdHeader) {
      thread_id = threadIdHeader;
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    const preview = document.querySelector('.markdown-preview');

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('data: ');

        for (const line of lines) {
          // 移除 line 末尾的 \n\n
          const data = line.replace(/\n\n$/, '');
          console.log(data);
          res_text.value += data;

          // 让 .markdown-preview 滚动到底部
          function animateScroll() {
            if (preview) {
              preview.scrollTop = preview.scrollHeight;
            }
          }
          requestAnimationFrame(animateScroll);
        }
      }
    }

  } catch (error) {
    console.error('创建 SSE 连接失败:', error);
    isLoading.value = false;
  }
};

// 提交问题
const submitQuestion = () => {
  console.log('提交问题:', question.value);
  connectSSE();
};
</script>

<template>
  <div class="chat-container">
    <VueMarkdownIt :content="res_text" class="markdown-preview" />
    <div class="chat-input">
      <textarea v-model="question" />
      <button @click="submitQuestion">Submit</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 90vw;
  height: calc(100vh - 20px);
  margin: 0 auto;
  padding: 10px;
  position: relative;
}

.markdown-preview {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  height: calc(100% - 60px);
  overflow-y: auto;
}

.chat-input {
  position: absolute;
  bottom: 10px;
  width: calc(100% - 20px);
}

.chat-input textarea {
  width: 100%;
  height: 50px;
  padding: 0;
  border: none;
}

.chat-input button {
  position: absolute;
  right: 0;
  bottom: 0;
}
</style>
