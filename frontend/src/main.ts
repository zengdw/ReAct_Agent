import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'vue-markdown-shiki/style'
import markdownPlugin from 'vue-markdown-shiki'

createApp(App).use(markdownPlugin).mount('#app')
