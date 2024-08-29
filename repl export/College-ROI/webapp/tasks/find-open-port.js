const portscanner = require('portscanner');
const _ = require('lodash');

const PORT_RANGE_START = process.env.SAUCELABS_PORT_RANGE_START || 9081;
const PORT_RANGE_END = process.env.SAUCELABS_PORT_RANGE_END || 9100;
const LOOPBACK_ADDRESS = '127.0.0.1';

async function isAvailable(port) {
  let status = await portscanner.checkPortStatus(port, LOOPBACK_ADDRESS);
  return status === 'closed';
}

async function findAvailablePort() {
  let port = _.random(PORT_RANGE_START, PORT_RANGE_END);
  if (!(await isAvailable(port))) {
    await findAvailablePort();
  } else {
    console.log(port);
  }
}
findAvailablePort();