const path = require('path');
const Handlebars = require('handlebars');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ImageminWebpWebpackPlugin= require("imagemin-webp-webpack-plugin");
const data = require('./src/data.json');

module.exports = {
  entry: './src/app.js',
  devtool: 'inline-source-map',
  devServer: {
    static: './dist',
    hot: false,
    liveReload: true
  },
  plugins: [
    new ImageminWebpWebpackPlugin({
      config: [
        {
          test: /\.(gif|png|jpe?g)$/i,
          options: {
            destination: 'dist/images',
          }
        }
      ]
    }),
    new HtmlWebpackPlugin({
      template: './src/index.html',
      minify: false
    })
  ],
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'dist'),
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.(html)$/,
        loader: "html-loader",
        options: {
          minimize: false,
          preprocessor: (content, loaderContext) => {
            let result;

            try {
              result = Handlebars.compile(content)({
                musicians: data.musicians
              });
            } catch (error) {
              loaderContext.emitError(error);

              return content;
            }

            return result;
          },
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.s[ac]ss$/i,
        use: ["style-loader", "css-loader", "sass-loader",],
      },
      {
        test: /\.(gif|png|jpe?g|svg|webp)$/i,
        type: 'asset/resource',
        use: [{
          loader: 'image-webpack-loader',
          options: {
            webp: {
              quality: 75
            }
          }
        }],
        generator: {
          filename: (pathData) => pathData.filename.substring(3) // Remove src from the path
        }
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[hash][ext][query]'
        }
      },
    ],
  }
};
