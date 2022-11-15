const { createProxyMiddleware } = require("http-proxy-middleware");
const fs = require('fs');

module.exports = function (app) {

  const rawdata = fs.readFileSync('src/deployment.json');
  const deployment = JSON.parse(rawdata);

  const backendBaseUrl = (() => {
    switch (deployment.env) {
      case 'mock':
        return 'http://localhost:3100/'; //use the mock server 
      case 'local':
        return 'http://localhost:5000/'; //use the local api server
      case 'dev':
        return 'https://devapi.xurlpay.org/v1/';
      case 'prd':
        return 'https://api.xurlpay.org/v1/';
    }
  })();


  app.use(
    createProxyMiddleware("/api", {
      target: backendBaseUrl,
      pathRewrite: {
        "^/api": "",
      },
    })
  );
};