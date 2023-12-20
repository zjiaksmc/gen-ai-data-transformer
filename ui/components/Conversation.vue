<script setup>
// import {EventStreamContentType} from '@microsoft/fetch-event-source'
// import { useAuthFetchEventSource } from '~/composables/fetch'

const { $i18n, $settings } = useNuxtApp()
const runtimeConfig = useRuntimeConfig()
const openaiApiKey = useApiKey()
const fetchingResponse = ref(false)
const messageQueue = []
let isProcessingQueue = false

const props = defineProps({
  conversation: {
    type: Object,
    required: true
  }
})

const processMessageQueue = () => {
  if (isProcessingQueue || messageQueue.length === 0) {
    return
  }
  if (!props.conversation.messages[props.conversation.messages.length - 1].author=='bot') {
    props.conversation.messages.push({content: '', author: 'bot'})
  }
  isProcessingQueue = true
  const nextMessage = messageQueue.shift()
  if (runtimeConfig.public.typewriter) {
    let wordIndex = 0;
    const intervalId = setInterval(() => {
      props.conversation.messages[props.conversation.messages.length - 1].message += nextMessage[wordIndex]
      wordIndex++
      if (wordIndex === nextMessage.length) {
        clearInterval(intervalId)
        isProcessingQueue = false
        processMessageQueue()
      }
    }, runtimeConfig.public.typewriterDelay)
  } else {
    props.conversation.messages[props.conversation.messages.length - 1].message += nextMessage
    isProcessingQueue = false
    processMessageQueue()
  }
}

let ctrl
const abortFetch = () => {
  if (ctrl) {
    ctrl.abort()
  }
  fetchingResponse.value = false
}
const fetchReply = async (message, tool, type) => {
  ctrl = new AbortController()

  if (message.tool == 'web_search') {
    message.tool_args = {
      user_agent: navigator.userAgent
    }
    message.type = 100
  } else if (message.tool == 'proprietary_search') {
    message.tool_args = null
    message.type = 110
  }

  const request_data = Object.assign({}, {
    message: message.content,
    tool: message.tool,
    tool_args: message.tool_args,
    type: message.type,
    session_id: props.conversation.session_id
  })
  // console.log(request_data)

  try {
    const { data, error } = await useAuthFetch('/copilot/chat/session/'+request_data.session_id, {
      method: 'POST',
      body: JSON.stringify(request_data)
    })
    if (!error.value) {

      props.conversation.messages.push({ content: data.value.conversation, author: 'bot' })
    }
    scrollChatWindow()
    fetchingResponse.value = false
  } catch (err) {
    showSnackbar(err.message)
  }
}

const grab = ref(null)
const scrollChatWindow = () => {
  if (grab.value === null) {
    return;
  }
  grab.value.scrollIntoView({behavior: 'smooth'})
}

const send = (message) => {
  fetchingResponse.value = true
  // if (props.conversation.messages.length === 0) {
  //   addConversation(props.conversation)
  // }
  if (Array.isArray(message)) {
    // props.conversation.messages.push(...message.map(i => ({conent: i.content, author: i.author})))
    console.log("Currently only support one message at a time.")
  } else {
    props.conversation.messages.push({ content: message.content, author: message.author })
  }
  fetchReply(message, message.tool, message.message_type)
  scrollChatWindow()
}
const stop = () => {
  abortFetch()
}

const snackbar = ref(false)
const snackbarText = ref('')
const showSnackbar = (text) => {
  snackbarText.value = text
  snackbar.value = true
}

const editor = ref(null)
const usePrompt = (prompt) => {
  // editor.value.usePrompt(prompt)
}

const deleteMessage = (index) => {
  // props.conversation.messages.splice(index, 1)
}

const toggleMessage = (index) => {
  // props.conversation.messages[index].is_disabled = !props.conversation.messages[index].is_disabled
}

const enableWebSearch = ref(false)


</script>

<template>
  <div v-if="conversation">
    <div
        v-if="conversation.loadingMessages"
        class="text-center"
    >
      <v-progress-circular
          indeterminate
          color="primary"
      ></v-progress-circular>
    </div>
    <div v-else>
      <div
          v-if="conversation.messages"
          ref="chatWindow"
      >
        <v-container>
          <v-row>
            <v-col
                v-for="(message, index) in conversation.messages" :key="index"
                cols="12"
            >
              <div
                  class="d-flex align-center"
                  :class="message.author=='bot' ? 'justify-start' : 'justify-end'"
              >
                <MessageActions
                    v-if="message.author=='user'"
                    :message="message"
                    :message-index="index"
                />
                <MsgContent
                  :message="message"
                  :index="index"
                />
                <MessageActions
                    v-if="message.author=='bot'"
                    :message="message"
                    :message-index="index"
                />
              </div>
            </v-col>
          </v-row>
        </v-container>

        <div ref="grab" class="w-100" style="height: 200px;"></div>
      </div>
    </div>
  </div>


  <v-footer
      app
      class="footer"
  >
    <div class="px-md-16 w-100 d-flex flex-column">
      <div class="d-flex align-center">
        <v-btn
            v-show="fetchingResponse"
            icon="close"
            title="stop"
            class="mr-3"
            @click="stop"
        ></v-btn>
        <MsgEditor ref="editor" :send-message="send" :disabled="fetchingResponse" :loading="fetchingResponse" />
      </div>
      <v-toolbar
          density="comfortable"
          color="transparent"
      >
        <!-- <Prompt v-show="!fetchingResponse" :use-prompt="usePrompt" /> -->
        <!-- <v-switch
            v-model="enableWebSearch"
            inline
            hide-details
            color="primary"
            :label="$t('webSearch')"
        ></v-switch> -->
      </v-toolbar>
    </div>
  </v-footer>
  <v-snackbar
      v-model="snackbar"
      multi-line
      location="top"
  >
    {{ snackbarText }}

    <template v-slot:actions>
      <v-btn
          color="red"
          variant="text"
          @click="snackbar = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>

</template>

<style scoped>
  .footer {
    width: 100%;
  }
</style>