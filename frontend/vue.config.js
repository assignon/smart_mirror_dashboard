  module.exports = {
  transpileDependencies: ["vuetify"],
  "devServer": {
    "proxy": {
      "^/": {
        "target": "http://18.118.114.216:8080/",
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
