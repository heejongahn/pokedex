import path from 'path';
import webpack from 'webpack';

import ExtractTextPlugin from 'extract-text-webpack-plugin';

const assetPath = './pokedex/assets';
const absAssetPath = path.resolve(assetPath);

const staticPath = './pokedex/static';
const absStaticPath = path.resolve(staticPath);

const plugins = [
  new ExtractTextPlugin('style.css'),
];

export default {
  entry: {
    bundle: `${absAssetPath}/main.js`,
  },
  output: {
    path: absStaticPath,
    publicPath: '/static/',
    filename: '[name].js',
  },
  resolve: {
    extensions: ['', '.js', '.styl']
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        include: [
          absAssetPath
        ],
        loader: 'babel',
        query: { presets: ['es2015'] }
      },
      {
        test: /\.styl$/,
        loader: ExtractTextPlugin.extract('style-loader', ['css-loader', 'stylus-loader'])
      },
    ]
  },
  plugins: plugins
};
