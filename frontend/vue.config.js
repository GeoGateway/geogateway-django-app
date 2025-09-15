const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    publicPath:
        process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:9000/static/geogateway_django_app/bundles/" : "/static/geogateway_django_app/bundles/",
    outputDir: '../geogateway_django_app/static/geogateway_django_app/bundles',

    devServer: {
        allowedHosts: 'all'
    },
    configureWebpack: {
        optimization: {

            splitChunks: {
                cacheGroups: {
                    vendors: {
                        name: 'chunk-vendors',
                        test: /[\\/]node_modules[\\/]/,
                        priority: -10,
                        chunks: 'initial'
                    },
                }
            }
        }
    },

    chainWebpack: config => {

        config.module
            .rule('scss')
            .test(/\.scss$/,)
            .use('sass-loader')
            .loader('css-loader')
            .loader('vue-style-loader')
            .end()

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{
                filename: 'webpack-stats.json',
                path: '../geogateway_django_app/static/geogateway_django_app/bundles/'
            }])

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .host('0.0.0.0')
            .port(9000)
            .hot(true)
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})
        
        config.devServer.set('watchFiles', {
            paths: ['**/*'],
            options: {
                usePolling: true,
                interval: 1000
            }
        })
    }
};
