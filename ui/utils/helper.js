
export const getDefaultConversationData = async () => {
    const { $i18n } = useNuxtApp()
    const conversations = await getConversations()
    if (conversations.length <= 0) {
        const conversation = await createConversation()
        addConversation(conversation)
        return conversation
    } else {
        const conversation = await loadConversation(conversations[0].session_id)
        return conversation
    }
}

export const getConversations = async () => {
    const user = useUser()
    const { data, error } = await useAuthFetch('/copilot/chat/session/?user_id='+user.value.username+'&is_active=1')
    if (!error.value) {
        return data.value.session
    }
    return []
}

export const createConversation = async() => {
    const user = useUser()
    const request_data = Object.assign({}, {
        user_id: user.value.username,
        email: user.value.email
    })
    const { data, error } = await useAuthFetch('/copilot/chat/session/', {
        method: 'POST',
        body: JSON.stringify(request_data)
    })
    if (!error.value) {
        const conversation = Object.assign(data.value.session, {
            messages: data.value.conversation,
            loadingMessages: false
        })
        return conversation
    } else {
        throw new Error(`Failed to create conversation.`);
    }
}

export const loadConversation = async (session_id) => {
    const { data, error } = await useAuthFetch('/copilot/chat/session/' + session_id)
    if (!error.value) {
      const conversation = Object.assign(data.value.session, {
        messages: data.value.conversation,
        loadingMessages: false
      })
      return conversation
    }
  }

export const addConversation = (conversation) => {
    const conversations = useConversations()
    conversations.value = [conversation, ...conversations.value]
}

export const genTitle = async (conversationId) => {
    // const { $i18n, $settings } = useNuxtApp()
    // const openaiApiKey = useApiKey()
    // const { data, error } = await useAuthFetch('/api/gen_title/', {
    //     method: 'POST',
    //     body: {
    //         conversationId: conversationId,
    //         prompt: $i18n.t('genTitlePrompt'),
    //         openaiApiKey: $settings.open_api_key_setting === 'True' ? openaiApiKey.value : null,
    //     }
    // })
    // if (!error.value) {
    //     const conversations = useConversations()
    //     let index = conversations.value.findIndex(item => item.id === conversationId)
    //     if (index === -1) {
    //         index = 0
    //     }
    //     conversations.value[index].topic = data.value.title
    //     return data.value.title
    // }
    return null
}

export const fetchUser = async () => {
    return useMyFetch('/api/account/user/')
}

export const setUser = (userData) => {
    const user = useUser()
    user.value = userData
}

export const logout = () => {
    const user = useUser()
    user.value = null
    return navigateTo('/api/account/signin');
}