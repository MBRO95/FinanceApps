import 'reflect-metadata';
import 'zone.js/dist/zone-node';
import { enableProdMode } from '@angular/core';
import { join } from 'path';
import { json, urlencoded } from 'body-parser';
import { ngExpressEngine } from '@nguniversal/express-engine';
import { provideModuleMap } from '@nguniversal/module-map-ngfactory-loader';
import { readFileSync } from 'fs';
import * as compression from 'compression';
import * as express from 'express';
import * as proxy from 'http-proxy-middleware';
import { endpoints } from './endpoints';

logger.time('server-startup');

enableProdMode();

const APP = express();
const PKG = require('./package.json');
const PORT = process.env.PORT || 8080;
const PATH_DIST = join(process.cwd(), 'dist');
const PATH_BROWSER = join(PATH_DIST, 'browser');
const PATH_INDEX_TEMPLATE = join(PATH_BROWSER, 'index.html');
const PATH_STATIC_PKG_ROUTE = `/pkg/${PKG.version}/web`;
const PATH_STATIC_ASSET = '/assets';
const PATH_ASSETS = join(PATH_BROWSER, '/assets');
const SOURCE_INDEX_TEMPLATE = readFileSync(PATH_INDEX_TEMPLATE, 'utf-8').toString();
const { AppServerModuleNgFactory, LAZY_MODULE_MAP } = require('./dist/server/main');

APP.use(vgBaseHref({ pkg: PKG }));
APP.engine(
  'html',
  ngExpressEngine({
    bootstrap: AppServerModuleNgFactory,
    providers: [provideModuleMap(LAZY_MODULE_MAP)]
  })
);
APP.set('view engine', 'html');
APP.set('views', PATH_BROWSER);
APP.use(compression());
APP.use(urlencoded({ extended: false }));
APP.use(json());
APP.use(
  PATH_STATIC_PKG_ROUTE,
  express.static(PATH_BROWSER, {
    maxAge: '1y',
    fallthrough: false
  })
);
APP.use(
  PATH_STATIC_ASSET,
  express.static(PATH_ASSETS, {
    maxAge: '1y',
    fallthrough: false
  })
);

/*********************************/
/* Setup API endpoint forwarding */
/*********************************/
const API_REGION = process.env.API_REGION || 'development';
endpoints.forEach((endpoint) => {
  const proxyConfig = {
    target: endpoint.regions[API_REGION],
    ws: true,
    changeOrigin: true,
    pathRewrite: {
      [`^${endpoint.uri}`]: '/'
    }
  };
  APP.use(proxy(`${endpoint.uri}`, proxyConfig));
});


/***********************************/
/* Server Static Route For Favicon */
/***********************************/
APP.use('/favicon.ico', express.static(join(PATH_BROWSER, 'favicon.ico')));

/******************************************/
/* Disable X-POWERED-BY Header By Default */
/******************************************/
APP.disable('x-powered-by');

/***********************************************/
/* All regular routes use the Universal engine */
/***********************************************/
APP.get('*', (req, res) => {
  const document = SOURCE_INDEX_TEMPLATE.replace(/"\/"/, `"${baseHref}"`);
  res.header('Content-Security-Policy', csp);
  res.header('X-Frame-Options', 'SAMEORIGIN');
  res.header('X-XSS-Protection', '1; mode=block');
  res.render('index', { req, document });
});

/****************************/
/* Start Up The Node Server */
/****************************/
APP.listen(PORT, () => {
  logger.timeEnd('server-startup');
  logger.info(`Node application ${PKG.name} has started their node server on port ${PORT}`);
});
/**********************/
/* Express Server End */
/**********************/
