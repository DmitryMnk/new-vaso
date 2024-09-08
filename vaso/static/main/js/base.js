function getScrollbarWidth() {
    return window.innerWidth - document.documentElement.clientWidth;
}

function getCSRF() {
    const cookies = document.cookie.split(';');
    var token;
    var cookiesDict = {}
    for (const cookie of cookies) {
        const cookieList = cookie.split('=');
        const key = cookieList[0].trim();
        const value = cookieList[1].trim();
        if (key == 'csrftoken') {
            token = value;
            break
        }
    }
    return token;

}

async function sendCodeAPI(url, data) {
    const csrf = getCSRF();
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    return {
        'response': response,
        'data': responseData
    }
}

function phoneInputCorrecting(input) {
    const value = input.value;
    const lastSym = value[value.length - 1]
    const subValue = value.slice(0, -1);

    if (lastSym < '0' || lastSym > '9') {
        input.value = subValue;
    }

    if (value.length > 12) {
        input.value = subValue;
    }
}


export {
    getScrollbarWidth, 
    sendCodeAPI, 
    getCSRF,
    phoneInputCorrecting,
}