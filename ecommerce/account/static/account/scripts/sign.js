// Set up the Login / Register page swap
const toReg = document.querySelector('#toRegister'),
    toLog = document.querySelector('#toLogin');

toReg.addEventListener('mouseover', e => {
    document.querySelector('label[for="toRegister"]').style.opacity = 1;
})
toReg.addEventListener('mouseout', e => {
    document.querySelector('label[for="toRegister"]').style.opacity = '';
})
toLog.addEventListener('mouseover', e => {
    document.querySelector('label[for="toLogin"]').style.opacity = 1;
})
toLog.addEventListener('mouseout', e => {
    document.querySelector('label[for="toLogin"]').style.opacity = '';
})

const hide = (querySelector, toLeft=true) => {
    el = document.querySelector(querySelector);
    for (const child of el.querySelectorAll('input')) {
        child.setAttribute('tabindex', -1);
    }
    if (toLeft) {
        el.style.translate = '-120vw 0 0';
    } else {
        el.style.translate = '120vw 0 0';
    }
};
const show = (querySelector, toLeft=true) => {
    el = document.querySelector(querySelector);
    for (const child of el.querySelectorAll('input')) {
        child.setAttribute('tabindex', 0);
    }
    if (toLeft) {
        el.style.translate = '0 0 0';
    } else {
        el.style.translate = '0 0 0';
    }
};

toLog.onclick = (e)=> {
    toLog.style.animation = "none";
    hide('.page_2', false);
    hide('#toLogin', false);
    hide('label[for="toLogin"]', false);
    setTimeout(()=>{
        toReg.style.animation = "";
        show('.page_1', true);
        show('#toRegister', false);
        show('label[for="toRegister"]', false);
    }, 350)
}
toReg.onclick = (e)=> {
    toReg.style.animation = "none";
    hide('.page_1', true);
    hide('#toRegister', true);
    hide('label[for="toRegister"]', true);
    setTimeout(()=>{
        toLog.style.animation = "";
        show('.page_2', false);
        show('#toLogin', false);
        show('label[for="toLogin"]', false);
    }, 350);
}
toLog.style.animation = "none";
hide('#toLogin', false);
hide('label[for="toLogin"]', false);

// Custom form handlers
// const formReg = document.querySelector('input[value="register"]').parentElement,
//     formLog = document.querySelector('input[value=login]').parentElement;

// formReg.onsubmit = async e => {
//     e.preventDefault();
//     const username = formReg.querySelector('input[name=username]').value,
//         email = formReg.querySelector('input[name=email]').value,
//         password = formReg.querySelector('input[name=password]').value,
//         confirmation = formReg.querySelector('input[name=confirmation]').value,
//         action = formReg.querySelector('input[name=action]').value;
//     // const url = `/account/sign/?username=${username}&email=${email}&password=${password}&confirmation=${confirmation}&action=${action}`
//     const url = "/account/sign/?username=asd&email=test@example.com&password=testUser123&confirmation=testUser12312&action=register"
//     resp = await fetch(url, {
//         method: 'POST',
//         headers: {
//             'Accept': 'application/json',
//             'X-CSRFToken': formReg.querySelector('input[name="csrfmiddlewaretoken"]').value
//         }
//     });
//     console.log(resp);
// }