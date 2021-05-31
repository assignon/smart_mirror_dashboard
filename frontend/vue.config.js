// // const path = require('path');
// module.exports = {
//   transpileDependencies: ["vuetify"],
//   "devServer": {
//     "proxy": {
//       "^/": {
//         "target": "http://127.0.0.1:8000/",
//         // "target": "https://accountancy-tsgf2.ondigitalocean.app/",
//         "ws": false
//       }
//     }
//   },
//   "outputDir": "./dist/",
//   "assetsDir": "static",
//   "transpileDependencies": [
//     "vuetify"
//   ]
// };

module.exports = {
  transpileDependencies: ["vuetify"],
  devServer: {
        proxy: 'http://127.0.0.1:5000/',
    }
};