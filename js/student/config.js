/* Firebase web app settings are public identifiers, not service-account secrets.
 * The Worker origin is intended by the reviewed contract; deployment is unverified. Do not add private credentials to this file. */
export const studentConfig = Object.freeze({
  firebase: Object.freeze({
    apiKey: 'AIzaSyBEPKUDm2eh6rPZxaWolAnOL5JaQKLPDa8',
    authDomain: 'ekguru-premium.firebaseapp.com',
    projectId: 'ekguru-premium',
    storageBucket: 'ekguru-premium.firebasestorage.app',
    messagingSenderId: '496486998098',
    appId: '1:496486998098:web:3de9073998de6e6d94ff8b'
  }),
  authActionUrl: null,
  workerOrigin: 'https://api.ekguru.shop',
  routes: Object.freeze({ dashboard: null, catalogue: null, purchases: null, deleteAccount: null })
});
