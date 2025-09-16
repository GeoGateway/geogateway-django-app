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
        resolve: {
            alias: {
                vue: '@vue/compat'
            }
        },
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

        // SCSS configuration - removing potentially problematic custom rule
        // Vue CLI handles SCSS automatically

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{
                filename: 'webpack-stats.json',
                path: '../geogateway_django_app/static/geogateway_django_app/bundles/'
            }])

        config.resolve.alias
            .set('__STATIC__', 'static')
            .set('vue', '@vue/compat')

        config.devServer
            .host('0.0.0.0')
            .port(9000)
            .hot(true)
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})
        
        // Simplified watchFiles configuration
        config.devServer.set('watchFiles', ['src/**/*'])
    }
};
