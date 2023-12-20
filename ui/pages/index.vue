<script setup>
definePageMeta({
  middleware: ["auth"],
  path: '/:session_id?',
  keepalive: true
})

const { $i18n } = useNuxtApp()
const runtimeConfig = useRuntimeConfig()
const drawer = useDrawer()
const route = useRoute()
const conversations = useConversations()
const conversation = ref(await getDefaultConversationData())
const creatingConversation = ref(false)
const navTitle = ref('copilot session: '+conversation.value.session_name)


const createNewConversation = async() => {
  creatingConversation.value = true
  navTitle.value = 'copilot session:'
  conversation.value = await createConversation()
  navTitle.value = 'copilot session: '+conversation.value.session_name
  creatingConversation.value = false
  addConversation(conversation.value)
  // if (route.path == '/') {
  //   return navigateTo('/?new')
  // }
  // return navigateTo('/')
  return navigateTo('/'+conversation.value.session_id)
}

onMounted(async () => {
  if (route.params.session_id) {
    conversation.value.loadingMessages = true
    navTitle.value = 'copilot session:'
    conversation.value = await loadConversation(route.params.session_id)
    navTitle.value = 'copilot session: '+conversation.value.session_name
    conversation.value.loadingMessages = false
  }
})

</script>

<template>
  <v-app-bar>
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

    <v-toolbar-title>{{ navTitle }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn
        :title="$t('newConversation')"
        icon="add"
        @click="createNewConversation"
        class="d-md-none ma-3"
    ></v-btn>
    <v-btn
        variant="outlined"
        class="text-none d-none d-md-block"
        @click="createNewConversation"
    >
      {{ $t('newConversation') }}
    </v-btn>

  </v-app-bar>

  <v-main>
    <div
        v-if="creatingConversation"
        class="text-center"
    >
      <v-progress-circular
          indeterminate
          color="primary"
      ></v-progress-circular>
    </div>
    <div v-else>
      <!-- <Welcome v-if="!route.params.session_id && conversation.messages.length === 0" /> -->
      <Welcome v-if="conversation.messages.length === 0" />
      <Conversation :conversation="conversation" />
    </div>
  </v-main>
</template>