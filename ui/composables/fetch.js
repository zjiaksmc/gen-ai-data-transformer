export const useMyFetch = (url, options = {}) => {
    let defaultOptions = {
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token 7209965eaa3d873ea0a53edf7a20346066485233'
        }
    }
    if (process.server) {
        defaultOptions.baseURL = process.env.SERVER_DOMAIN
    } else {
        defaultOptions.baseURL = 'https://aidf-backend-dot-docai-warehouse-demo.uc.r.appspot.com'
    }
    return useFetch(url, Object.assign(defaultOptions, options))
}
export const useAuthFetch = async (url, options = {}) => {
    const res = await useMyFetch(url, options)
    if (res.error.value && res.error.value.status === 401) {
        await logout()
    }
    return res
}