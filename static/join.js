/*
    https://developer.mozilla.org/en-US/docs/Mozilla/Persona/Quick_Setup
*/

var signinLink = document.getElementById('signin');
if (signinLink) {
    signinLink.onclick = function() { navigator.id.request(); };
}

var signinLink = document.getElementById('signin2');
if (signinLink) {
    signinLink.onclick = function() { navigator.id.request(); };
}

// Step 3: Watch for login and logout actions

var currentUser = null;

function simpleXhrSentinel(xhr) {
    return function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                // reload page to reflect new login state
                window.location.reload();
            }
            else {
                alert("XMLHttpRequest error: " + xhr.status);
                navigator.id.logout();
                // alert("XMLHttpRequest error: " + xhr.status);
            }
        }
    };
}

function verifyAssertion(assertion) {
    // Your backend must return HTTP status code 200 to indicate successful
    // verification of user's email address and it must arrange for the binding
    // of currentUser to said address when the page is reloaded
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/persona/signin", true);
    // see http://www.openjs.com/articles/ajax_xmlhttp_using_post.php
    var param = "assertion=" + assertion;
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("Content-length", param.length);
    xhr.setRequestHeader("Connection", "close");
    xhr.send(param); // for verification by your backend

    xhr.onreadystatechange = simpleXhrSentinel(xhr); 
}

function signoutUser() {
    // Your backend must return HTTP status code 200 to indicate successful
    // sign out (usually the resetting of one or more session variables) and
    // it must arrange for the binding of currentUser to 'null' when the page
    // is reloaded
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/persona/signout", true);
    xhr.send(null);
    xhr.onreadystatechange = simpleXhrSentinel(xhr);
}

// Go!
navigator.id.watch( {
    loggedInUser: currentUser,
        onlogin: verifyAssertion,
        onlogout: signoutUser
    } );