  module.exports = {
  transpileDependencies: ["vuetify"],
  "devServer": {
    "proxy": {
      "^/": {
        "target": "http://0.0.0.0:8000/",
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
//   transpileDependencies: ["vuetify"]
// };
