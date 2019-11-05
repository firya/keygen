const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const historyApiFallback = require('connect-history-api-fallback');
const postcssPresetEnv = require('postcss-preset-env');
const postcssImport = require('postcss-import');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
  entry: [
    './src/index.js',
  ],
  output: {
    publicPath: ``,
    path: path.resolve(__dirname, `dist`),
    filename: 'static/js/scripts.js',
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.(js|jsx)?$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', "@babel/preset-react"],
            plugins: [
              [
                "@babel/plugin-proposal-decorators",
                { legacy: true }
              ],
              [
                "@babel/plugin-proposal-class-properties",
                {
                  decoratorsBeforeExport: false,
                  legacy: true
                }
              ]

            ]
          }
        }
      },
      {
        test: /\.css$/,
        include: [/node_modules/],
        use: [
          {
            loader: "style-loader",
          },
          {
            loader: "css-loader",
            options: {
              modules: false,
            },
          },
        ],
      },
      {
        test: /\.css$/,
        include: path.resolve(__dirname, "src"),
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {}
          },
          {
            loader: "css-loader",
            options: {
              sourceMap: true,
              url: false
            }
          },
          {
            loader: "postcss-loader",
            options: {
              ident: "postcss",
              sourceMap: true,
              plugins: () => [
                postcssImport(),
                postcssPresetEnv({
                  browsers: 'last 2 versions',
                  features: {
                    'nesting-rules': true
                  },
                }),
                require("cssnano")({
                  preset: [
                    "default",
                    {
                      discardComments: {
                        removeAll: true
                      }
                    }
                  ]
                })
              ]
            }
          }
        ]
      }, {
        test: /\.svg$/,
        loader: 'vue-svg-loader',
      },
    ]
  },
  plugins: [
    new BrowserSyncPlugin({
      server: {
        baseDir: './dist',
        middleware: [historyApiFallback()]
      },
      port: 3000,
      open: false,
      notify: false,
    }),
    new MiniCssExtractPlugin({
      filename: "static/css/styles.css",
    }),
    new VueLoaderPlugin()
  ],
  watchOptions: {
    ignored: ['node_modules', 'info']
  }
};
