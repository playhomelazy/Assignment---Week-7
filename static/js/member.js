function loading(){
    let findusername = document.getElementById("finduser").value;
    let src = "http://127.0.0.1:3000/api/users?username="+findusername;
    fetch(src).then(function (response) {
        return response.json();
    }).then(function (result) {
        let text = document.getElementById("member_name");
        if(result["data"]!=null && findusername!=''){
            text.textContent = result["data"]["name"]+" ("+result["data"]["username"]+")";
        }
        else{
            text.textContent = "查無此會員";
        }
    })
    }