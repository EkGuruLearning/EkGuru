// The public bundle contains only the official Firebase browser SDK exports used by the student UI.
export { initializeApp, getApps, getApp } from 'firebase/app';
export { getAuth, onAuthStateChanged, onIdTokenChanged, signInWithEmailAndPassword,
  createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider, sendPasswordResetEmail,
  sendEmailVerification, applyActionCode, verifyPasswordResetCode, confirmPasswordReset,
  signOut, updateProfile, setPersistence, browserLocalPersistence, browserSessionPersistence,
  checkActionCode } from 'firebase/auth';
