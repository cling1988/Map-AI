// vite.config.js
export default {
    // config options
    esbuild: {
        supported: {
            'top-level-await': true //browsers can handle top-level-await features
        },
    },
    build: {
        outDir: '../app/dist'
    }
}