
export const useModels = () => useState('models', () => getStoredModels())

export const useCurrentModel = () => useState('currentModel', () => getCurrentModel())

export const useApiKey = () => useState('apiKey', () => getStoredApiKey())

export const useConversations = () => useState('conversations', () => [])

export const useUser = () => useState('user', () => null)

export const useDrawer = () => useState('drawer', () => false)

// export const useColorMode = () => useState('colorMode', () => Object.assign({}, {
//     preference: 'light',
//     value: 'light',
//     unknow: false,
//     forced: false
// }))