<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { marked } from 'marked';

const question = ref('');
const response = ref('');
const isConnecting = ref(false);
const eventSource = ref<EventSource | null>(null);

// 解析 Markdown 为 HTML
const parsedMarkdown = computed(() => {
  if (!question.value.trim()) return '';
  return marked(question.value);
});

// SSE 连接函数
const connectSSE = () => {
  if (!question.value.trim()) {
    return;
  }

  // 关闭之前的连接
  if (eventSource.value) {
    eventSource.value.close();
  }

  isConnecting.value = true;
  response.value = '';

  try {
    // 构建带参数的 URL
    const params = new URLSearchParams({
      question: question.value
    });
    const url = `http://127.0.0.1:8081/sse?${params.toString()}`;
    
    eventSource.value = new EventSource(url);

    // 连接建立
    eventSource.value.onopen = (event) => {
      console.log('SSE 连接已建立', event);
    };

    // 接收消息
    eventSource.value.onmessage = (event) => {
      console.log('收到消息:', event.data);
      response.value += event.data;
    };

    // 处理错误
    eventSource.value.onerror = (event) => {
      console.error('SSE 连接错误:', event);
      isConnecting.value = false;
      if (eventSource.value) {
        eventSource.value.close();
        eventSource.value = null;
      }
    };

  } catch (error) {
    console.error('创建 SSE 连接失败:', error);
    isConnecting.value = false;
  }
};

// 停止 SSE 连接
const stopSSE = () => {
  if (eventSource.value) {
    eventSource.value.close();
    eventSource.value = null;
  }
  isConnecting.value = false;
};

// 提交问题
const submitQuestion = () => {
  console.log('提交问题:', question.value);
  connectSSE();
};

// 组件卸载时清理连接
onUnmounted(() => {
  if (eventSource.value) {
    eventSource.value.close();
  }
});
</script>

<template>
  <div class="chat-container">
    <div v-html="parsedMarkdown" class="markdown-preview"></div>
    <div class="chat-input">
      <textarea v-model="question" />
      <button @click="submitQuestion">Submit</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 100vw;
  height: 100vh;
}

.chat-input {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}

.chat-input textarea {
  width: 100%;
  height: 50px;
}

.chat-input button {
  position: absolute;
  right: 0;
  bottom: 0;
}
.markdown-preview {
  height: 99%;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  line-height: 1.6;
}

.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3,
.markdown-preview h4,
.markdown-preview h5,
.markdown-preview h6 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #333;
}

.markdown-preview p {
  margin-bottom: 10px;
}

.markdown-preview code {
  background-color: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.markdown-preview pre {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

.markdown-preview blockquote {
  border-left: 4px solid #ddd;
  padding-left: 15px;
  margin: 10px 0;
  color: #666;
}
</style>
