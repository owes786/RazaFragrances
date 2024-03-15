function FormValidation(){

    var flag = 1;

    let FName = document.getElementById('FName').value.trim();
    let LName = document.getElementById('LName').value.trim();
    let MNumber = document.getElementById('MNumber').value.trim();
    let Email = document.getElementById('Email').value.trim();
    let Password = document.getElementById('Password').value.trim();
    let CPassword = document.getElementById('CPassword').value.trim();
    FirstNameValidation()
    LastNameValidation()
    MobileNumberValidation()
    EmailValidation()
    PasswordValidation()
    ConfirmPasswordValidation()

    
                                // This function Validate First Name field
    function FirstNameValidation(){
        if (FName === ""){
            document.getElementById('ferror').innerHTML ="First Name Can't black!";
            flag = 1;
        }else if(FName.length <= 3){
            document.getElementById('ferror').innerHTML ="Name must be contain minimum 2 Characters";
            flag = 1;
        }else{
            document.getElementById('ferror').innerHTML ="";
            flag = 0;
        }
    }

                                // This function Validate Last Name field
    function LastNameValidation(){
        if (LName === ""){
            document.getElementById('lerror').innerHTML ="Last Name Can't black!";
            flag = 1;
        }else if(LName.length <= 3){
            document.getElementById('lerror').innerHTML ="Name must be contain minimum 2 Characters";
            flag = 1;
        }else{
            document.getElementById('lerror').innerHTML ="";
            flag = 0;
        }
    }

                                // This function Validate Mobile Number field
    function MobileNumberValidation(){
        if (MNumber == ''){
            document.getElementById('NumberError').innerHTML = "Mobile Number Can't black!";
            flag = 1;
        }else if(MNumber.length != 10){
            document.getElementById('NumberError').innerHTML ="Incorrect mobile Number!";
            flag = 1;
        }else{
            document.getElementById('NumberError').innerHTML = "";
            return true;
            flag = 0;
        }
    }

                                // This function Validate Email field
    function EmailValidation(){
        var atposition = Email.indexOf('@')
        var dotposition = Email.indexOf('.')
        if (Email == ''){
            document.getElementById('EmailError').innerHTML = "Email Can't black!";
            flag = 1;
        }else if(atposition < 1 || dotposition < atposition + 2 || dotposition+2>=Email.length){
            document.getElementById('EmailError').innerHTML = "Invalid Email Address!"
            flag = 1;
        }else{
            document.getElementById('EmailError').innerHTML = "";
            return true;
            flag = 0;
        }
    }
    
                                // This function Validate Password field
    function PasswordValidation(){
        if (Password == ""){
            document.getElementById('PasswordError').innerHTML ="Password Can't black!";
            flag = 1;
        }else if(Password.length <= 6){
            document.getElementById('PasswordError').innerHTML ="Password must be contain minimum 6 Characters";
            flag = 1;
        }else if(Password != CPassword){
            document.getElementById('PasswordError').innerHTML = "Password does not Match!"
            flag = 1;
        }else{
            document.getElementById('PasswordError').innerHTML ="";
            return true;
            flag = 0;
        }
    }

                                // This function Validate Confirm Password field
    function ConfirmPasswordValidation(){
        if (CPassword == ""){
            document.getElementById('CPasswordError').innerHTML ="Confirm Password Can't black!";
            flag = 1;
        }else if(CPassword.length <= 6){
            document.getElementById('CPasswordError').innerHTML ="Password must be contain minimum 6 Characters";
            flag = 1;
        }else if(CPassword !== Password){
            document.getElementById('CPasswordError').innerHTML = "Password does not Match!"
            flag = 1;
        }else{
            document.getElementById('CPasswordError').innerHTML ="";
            return true;
            flag = 0;
        }
    }


    if (flag == 1){
        return false;
    }else{
        return true;
    }
    
}