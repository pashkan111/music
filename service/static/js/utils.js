function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
  }
    return cookieValue;
}

console.log(111111)
const csrf_token = getCookie('csrftoken')

async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache', 
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFTOKEN":  csrftoken
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer', 
        body: JSON.stringify(data) 
    });
      return await response.json(); 
  }