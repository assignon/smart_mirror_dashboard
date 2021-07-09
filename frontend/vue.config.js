  module.exports = {
  transpileDependencies: ["vuetify"],
  "devServer": {
    "proxy": {
      "^/": {
        "target": "http://18.223.7.196/",
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
