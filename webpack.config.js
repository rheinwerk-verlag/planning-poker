'use strict'
const path = require('path');
const {VueLoaderPlugin} = require('vue-loader');
module.exports = {
    mode: 'production',
    entry: {
        'poker-session': './planning_poker/assets/js/poker-session.js',
        'header-app': './planning_poker/assets/js/header-app.js',
    },
    output: {
        path: path.resolve(__dirname, "planning_poker/static/planning_poker/js/"),
        publicPath: "/static/",
        filename: "[name].js"
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: 'vue-loader'
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    }
};
