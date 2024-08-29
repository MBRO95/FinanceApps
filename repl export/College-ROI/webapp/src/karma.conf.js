const OS = require('os');
const path = require('path');
const ENV = require('../environment-variables');
const chromeDrivers = require('vg-chrome-drivers');
const PROTRACTOR_CHROME_DRIVER = chromeDrivers(ENV.PLATFORM);
const child_process = require('child_process');
const LOCAL_PLUGINS = [require('karma-chrome-launcher')];
const REMOTE_PLUGINS = [require('karma-webdriver-launcher')];

module.exports = function(config) {
  setTimeout(() => openBrowser(config.buildWebpack.options.codeCoverage), 5000);
  config.set({
    hostname: ENV.HOSTNAME,
    port: ENV.PORT,
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-jasmine-html-reporter'),
      require('karma-coverage-istanbul-reporter'),
      require('@angular-devkit/build-angular/plugins/karma'),
      require('karma-junit-reporter'),
      require('karma-htmlfile-reporter'),
      ...(ENV.ENVIRONMENT_IS_LOCAL ? LOCAL_PLUGINS : REMOTE_PLUGINS)
    ],
    client: {
      clearContext: false,  // leave Jasmine Spec Runner output visible in browser
      jasmine: {
        timeoutInterval: 10000 // default value in jasmine
      }
    },
    coverageIstanbulReporter: {
      dir: ENV.TEST_UNIT_COVERAGE_REPORT_DIRECTORY,
      reporters: ENV.KARMA_CONF.COVERAGE_REPORTERS,
      fixWebpackSourcePaths: true,
      thresholds: {
        global: {
          statements: 100,
          lines: 100,
          branches: 100,
          functions: 100
        },
        each: {
          statements: 100,
          lines: 100,
          branches: 100,
          functions: 100
        }
      }
    },
    reporters: ENV.KARMA_CONF.REPORTERS,
    htmlReporter: {
      outputFile: ENV.REQUIREMENTS_EVIDENCE_FILE,
      pageTitle: 'Requirements Evidence',
    },
    colors: true,
    logLevel: config.LOG_INFO,
    concurrency: Infinity,
    allScriptsTimeout: 120000,
    captureTimeout: 210000,
    browserDisconnectTolerance: 3,
    browserDisconnectTimeout: 210000,
    browserNoActivityTimeout: 210000,
    processKillTimeout: 120000,
    chromeDriver: PROTRACTOR_CHROME_DRIVER,
    customLaunchers: ENV.KARMA_CONF.BROWSERS,
    browsers: Object.keys(ENV.KARMA_CONF.BROWSERS),
    junitReporter: {
      outputDir: ENV.TEST_UNIT_REPORT_DIRECTORY
    },
    autoWatch: true,
    singleRun: true,
    retryLimit: 5
  });
};

function openBrowser(coverage = false) {
  // Wait for webpack to start and then try to open tests in a browswer
  if (ENV.ENVIRONMENT_IS_LOCAL || ENV.ENVIRONMENT_IS_DOCKER) {
    try {
      const testUrl = `http://${ENV.BASE_URL}/debug.html`;
      const coverageUrl = `file:///${path.join(
        __dirname,
        '../reports/coverage/lcov-report/index.html'
      )}`;
      const url = coverage ? coverageUrl : testUrl;

      if (OS.platform() === 'win32') {
        child_process.exec(`start chrome ${url}`, () => { });
      } else {
        child_process.exec(`open google-chrome ${url}`, () => { });
      }
    } catch (e) {
      console.warn('Unable to open browser.');
    }
  }
}
