/* global require, __dirname */
const path = require("path");
const webpack = require("webpack");

const src = path.resolve(__dirname, "./");
const dist = path.resolve(__dirname, "./dist");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

/* eslint-disable no-process-env */

const apiUrl = process.env.API_URL;

module.exports = env => {
  const DEBUG = !env || !env.prod;
  return {
    mode: DEBUG ? "development" : "production",
    context: src,
    cache: DEBUG,
    devtool: DEBUG ? "cheap-module-source-map" : "sourcemap",
    entry: {
      app: [src + "/app/index.js"],
    },
    output: {
      path: dist,
      filename: "[name].bundle.js",
    },
    resolve: {
      extensions: [".js", ".css"],
      modules: [
        src,
        path.join(__dirname, "./node_modules"),
      ],
      alias: {
        "@": src,
      },
    },
    module: {
      rules: [
        {
          test: /.js$/,
          exclude: {
            include: /node_modules/,
            exclude: [
              /node_modules[\\/]/,
            ]
          },
          loader: "babel-loader",
          query: {
            presets: [
              [require.resolve("@babel/preset-env"),
              {
                "targets": {
                  "chrome": "69",
                  "edge": "83",
                  "firefox": "78",
                }
              }],
            ],
            plugins: [
              [
                require.resolve("@babel/plugin-proposal-class-properties"),
                { loose: true },
              ],
              require.resolve("@babel/plugin-proposal-optional-chaining"),
            ],
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {},
            },
            {
              loader: "css-loader",
              options: {
                url: true,
                sourceMap: true,
              },
            },
          ],
        },
        {
          test: /\.(woff|woff2|eot|ttf|svg)$/,
          use: [
            {
              loader: "file-loader",
              options: {},
            },
          ],
        },      
      ]
    },
    devServer: {
      contentBase: dist,
      port: 13002,
      host: "0.0.0.0",
      disableHostCheck: true,
      historyApiFallback: true,
      compress: true,
      proxy: apiUrl ? {
        '/data': apiUrl,
        '/ws/display': {                
          target: apiUrl,
          ws: true,
        },
        '/img': apiUrl,
        '/surface': apiUrl
      } : null
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "[name].bundle.css",
        ignoreOrder: false, // Enable to remove warnings about conflicting order
      }),
      new CopyWebpackPlugin([
        {
          from: "index.html",
          to: "index.html",
        },
        {
          from: "img/**/*",
        },
      ]),
    ].filter(item => item),
    node: {
      __dirname: true,
    },
  };
};
