(function(){
      var config = {
    apiKey: "AIzaSyDLOiH17g5snabv2Ws7ieIrwPSCzgApDeg",
    authDomain: "swe-final.firebaseapp.com",
    databaseURL: "https://swe-final.firebaseio.com",
    projectId: "swe-final",
    storageBucket: "swe-final.appspot.com",
    messagingSenderId: "799899141517"
  };
  firebase.initializeApp(config);

    const txtEmail = document.getElementById('txtEmail');
    const txtPassword = document.getElementById('txtPassword');
    const btnLogin = document.getElementById('btnLogin');
    const btnSignUp = document.getElementById('btnSignup');
    const btnLogout = document.getElementById('btnLogout');
    // const uploadBtn = document.getElementById('uploadBtn');
    const containerHTML = "<form>\
                <div class=\"group\">  \
                    <input id=\"txtEmail\" required>\
                    <span class=\"highlight\"></span>\
                    <span class=\"bar\"></span>\
                    <label>Email</label>\
                </div>\
                <div class=\"group\">\
                    <input id=\"txtPassword\" type=\"password\" required>\
                    <span class=\"highlight\"></span>\
                    <span class=\"bar\"></span>\
                    <label>Password</label>\
                </div>\
            </form>\
            <button id=\"btnLogin\" class=\"btn btn-primary\">\
                Log in\
            </button>\
            <button id=\"btnSignup\" class=\"btn btn-outline-secondary\">\
               Sign up\
            </button>\
            <div id=\"errorMessage\"></div>"

    // uploadBtn.addEventListener('click', e=>{
    //     document.getElementById("codeForm");
    // })

    btnLogin.addEventListener('click', e => {
        const email = txtEmail.value;
        const pass = txtPassword.value;
        const auth = firebase.auth();
        const promise = auth.signInWithEmailAndPassword(email, pass);
        promise.catch(e=>console.log(e));
    });

    btnSignUp.addEventListener('click', e=> {
        const email = txtEmail.value;
        const pass = txtPassword.value;
        const auth = firebase.auth();
        if(!email.endsWith("@bison.howard.edu")){
            document.getElementById('errorMessage').innerHTML = "Use a bison Email";
        }else{
            const promise = auth.createUserWithEmailAndPassword(email, pass);
            promise.catch(e=>document.getElementById('errorMessage').innerHTML= e);
        }
    });
    
    btnLogout.addEventListener('click', e=>{
        firebase.auth().signOut();
        document.getElementById('container').innerHTML= containerHTML;
    });

    firebase.auth().onAuthStateChanged(firebaseUser => {
        if(firebaseUser) {
            console.log(firebaseUser);
            btnLogout.classList.remove('invisible');
            personName.classList.remove('invisible');
            var email = txtEmail.value;
            email = email.replace('@bison.howard.edu', '');
            email = email.replace('.', ' ');
            var userName = namify(email);
            document.getElementById('personName').innerHTML = userName;
            document.getElementById('container').innerHTML = null;
            document.getElementById('upload').classList.remove('invisible');
        }
        else {
            console.log(containerHTML);
            console.log('not logged in');
            btnLogout.classList.add('invisible');
            document.getElementById('upload').classList.add('invisible');
            document.getElementById('personName').innerHTML = null;
        }
    })

    function namify(str) {
    return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}
}())