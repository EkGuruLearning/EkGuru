import { studentConfig } from './config.js';
let connection;
export function configured() {
  const c = studentConfig.firebase;
  return !!(c && typeof c.apiKey === 'string' && c.apiKey && typeof c.authDomain === 'string' && c.authDomain && typeof c.projectId === 'string' && c.projectId && typeof c.appId === 'string' && c.appId);
}
export async function connect() {
  if (!configured()) throw new Error('AUTH_NOT_CONFIGURED');
  if (!connection) connection = import('./firebase-sdk.js').then(sdk => {
    const app = sdk.getApps().find(a => a.name === 'ekguru-student') || sdk.initializeApp(studentConfig.firebase, 'ekguru-student');
    return { sdk, auth: sdk.getAuth(app) };
  }).catch(error => { connection = null; throw error; });
  return connection;
}
export function actionSettings() {
  if (!studentConfig.authActionUrl) return undefined;
  const url = new URL(studentConfig.authActionUrl, location.origin);
  if (url.origin !== location.origin || url.pathname !== '/account/action/' || url.search || url.hash) throw new Error('INVALID_ACTION_URL');
  return { url: url.href, handleCodeInApp: false };
}
export async function watch(callback) {
  const { sdk, auth } = await connect();
  return sdk.onIdTokenChanged(auth, callback, () => callback(null));
}
