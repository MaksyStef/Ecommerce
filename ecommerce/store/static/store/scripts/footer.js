import * as base from './base.js';

let nlButtons = document.querySelectorAll('.newsletter-toggler');
for (const toggler of nlButtons) {
    toggler.onclick = () => base.toggleNewsletter(toggler);
}
nlButtons = document.querySelectorAll('.newsletter-button_sign')
for (const signButton of nlButtons) {
    signButton.onclick = () => base.signNewsletter();
}
nlButtons = document.querySelectorAll('.newsletter-button_unsign')
for (const unsignButton of nlButtons) {
    unsignButton.onclick = () => base.unsignNewsletter(toggler);
}