<script setup>
import copy from 'copy-to-clipboard'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  messageIndex: {
    type: Number,
    required: true
  },
  usePrompt: {
    type: Function,
    required: false
  },
  deleteMessage: {
    type: Function,
    required: false
  },
  toggleMessage: {
    type: Function,
    required: false
  }
})

const snackbar = ref(false)
const snackbarText = ref('')
const showSnackbar = (text) => {
  snackbarText.value = text
  snackbar.value = true
}

const copyMessage = () => {
  copy(props.message.message)
  showSnackbar('Copied!')
}

const editMessage = () => {
  // props.usePrompt(props.message.content)
}

const deleteMessage = async () => {
  // const { data, error } = await useAuthFetch(`/api/chat/messages/${props.message.id}/`, {
  //   method: 'DELETE'
  // })
  // if (!error.value) {
  //   props.deleteMessage(props.messageIndex)
  //   showSnackbar('Deleted!')
  // }
  // showSnackbar('Delete failed')
}

const toggle_message = async() => {
  // const msg = Object.assign({}, props.message)
  // msg.is_disabled = !msg.is_disabled
  // const { data, error } = await useAuthFetch(`/api/chat/messages/${props.message.id}/`, {
  //   method: 'PUT',
  //   body: JSON.stringify(msg),
  // })
  // if (!error.value) {
  //   props.toggleMessage(props.messageIndex)
  // }
  // showSnackbar('Toogle message failed')
}

function selectMessageIcon(message) {
  if (message.authoer=="bot") return ""
  if (message.type == 100) {
    return "travel_explore"
  } else if (message.type == 110) {
    return "local_library"
  } else if (message.type == 120) {
    return "article"
  } 
  return ""
}

const message_icon = selectMessageIcon(props.message)

</script>

<template>
  <v-menu>
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        v-if="message_icon"
        variant="text"
        class="ma-2"
      >
          <v-icon :icon="message_icon"></v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item
          @click="toggle_message()"
          title="toggle"
          :prepend-icon="message.is_disabled ? 'toggle_off' : 'toggle_on'"
      >
      </v-list-item>
    </v-list>
  </v-menu>
  <v-menu
  >
    <template v-slot:activator="{ props }">
      <v-btn
          v-bind="props"
          icon
          variant="text"
          class="mx-1 ma-2"
      >
        <v-icon icon="more_horiz"></v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item
          @click="copyMessage()"
          :title="$t('copy')"
          prepend-icon="content_copy"
      >
      </v-list-item>
      <!-- <v-list-item
          @click="editMessage()"
          :title="$t('edit')"
          prepend-icon="edit"
      >
      </v-list-item>
      <v-list-item
          @click="deleteMessage()"
          :title="$t('delete')"
          prepend-icon="delete"
      >
      </v-list-item> -->
    </v-list>
  </v-menu>

  <v-snackbar
      v-model="snackbar"
      location="top"
      timeout="2000"
  >
    {{ snackbarText }}
  </v-snackbar>
</template>

<style scoped>

</style>