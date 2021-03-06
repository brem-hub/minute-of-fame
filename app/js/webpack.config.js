var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: './app',
  mode: 'development',
  output: {
      path: path.resolve('../static/webpack_bundles/'),
      publicPath: '/static/webpack_bundles/',
      filename: "[name]-[hash].js"
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.SourceMapDevToolPlugin({}),
    new webpack.DefinePlugin({
        'DEBUG': (process.env.DEBUG || '1') === '1',
        'WS_PORT': (process.env.WS_PORT || '4321')
    })
  ]
}