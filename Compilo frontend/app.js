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

    btnLogin.addEventListener('click', e => {
        const email = txtEmail.value;
        const pass = txtPassword.value;
        const auth = firebase.auth();
        const promise = auth.signInWithEmailAndPassword(email, pass);
        promise.catch(e=>console.log(e.message));
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
    });

    firebase.auth().onAuthStateChanged(firebaseUser => {
        if(firebaseUser) {
            console.log(firebaseUser);
            btnLogout.classList.remove('invisible');
        }
        else {
            console.log('not logged in');
            btnLogout.classList.add('invisible');
        }
    })
}())