module.exports = {
  transpileDependencies: ["vuetify"],
  "devServer": {
    "proxy": {
      "^/": {
        "target": "http://127.0.0.1:5000/",
        // "target": "https://accountancy-tsgf2.ondigitalocean.app/",
        "ws": false
      }
    }
  },
  "outputDir": "./dist/",
  "assetsDir": "static",
  "transpileDependencies": [
    "vuetify"
  ]
};

// module.exports = {
//     devServer: {
//       proxy: 'http://127.0.0.1:5000'
//     },
//     "outputDir": "./dist/",
// }