const path = require("path");
const fs = require("fs");
const HtmlWebpackPlugin = require("html-webpack-plugin");
// const RemarkHTML = require("remark-html");
const webpack = require("webpack");

const dotenv = require('dotenv')

// this will update the process.env with environment variables in .env file
dotenv.config();

module.exports = {

  mode: 'development',
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    // filename: '[name].[contenthash].js',
    filename: 'index_bundle.js',
    publicPath: '/'
  },
  // resolve: {
  //   fallback: { 
  //     "buffer": require.resolve("buffer/")     
  //   },
  //   // alias: {
  //   //   react: path.resolve('./node_modules/react'),
  //   // },
  // },
  devServer: {
    static: {
      directory: path.resolve(__dirname, 'dist'),
    },
    port: 3001,
    // open: true,
    // hot: true,
    compress: true,
    // historyApiFallback: true,
    // https:{
    //   key: fs.readFileSync("clay-deeporb-20.local+3-key.pem"),
    //   cert: fs.readFileSync("clay-deeporb-20.local+3.pem"),
    //   ca: fs.readFileSync("ca.crt"),     
    // }
  },


  // Where files should be sent once they are bundled
  // entry: "./src/index.js",
  // output: {
  //   path: path.join(__dirname, "/dist"),
  //   filename: "index.bundle.js",
  // },
  // Rules of how webpack will take our files, compile & bundle them for the browser
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        include: path.resolve(__dirname, "src"),
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ],
  },
  plugins: [
    // new HtmlWebpackPlugin({ inject: false, template: "./src/index.html", favicon: "./src/favicon.ico" }),
    new HtmlWebpackPlugin( {template: "./src/index.html"}),
    // new HtmlWebpackPlugin(),
    //new HtmlWebpackPlugin({ inject: true, favicon: "./src/favicon.ico" }),
    new webpack.DefinePlugin({
      'process.env': JSON.stringify(process.env)
    }),
    // Work around for Buffer is undefined:
    // https://github.com/webpack/changelog-v5/issues/10
    // new webpack.ProvidePlugin({
    //     Buffer: ['buffer', 'Buffer'],
    // }),
  ],
};
