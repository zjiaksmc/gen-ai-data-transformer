import { createProxyMiddleware } from 'http-proxy-middleware'
export default defineEventHandler(async (event) => {
    await new Promise((resolve, reject) => {
        createProxyMiddleware({
            target: process.env.SERVER_DOMAIN,
            pathFilter: '/*',
        })(event.node.req, event.node.res, (err) => {
            if (err)
                reject(err)
            else
                resolve(true)
        })
    })
})
