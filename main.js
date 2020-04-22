mensaje = "";
websocket = new WebSocket("ws://170.253.15.165:6789/");
var id_cliente = undefined;

function gi(t){
    return document.getElementById(t);
}

websocket.onmessage = function (event) {
    mensaje = JSON.parse(event.data);
    console.log(event.data);

    switch(mensaje.type){
        case "wellcome":
            id_cliente = mensaje.dst;
        case "msg":
            if(mensaje.src == 0){
                gi("chatArea").innerHTML += "<br><div class='sysMsg chatMsg'>" + mensaje.data + "</div>";
            }
            else if(mensaje.src == id_cliente){
                gi("chatArea").innerHTML += "<br><div class='myMsg chatMsg'>" + mensaje.data + "</div>";
            }
            else{
                gi("chatArea").innerHTML += "<br><div class='yourMsg chatMsg'>" + mensaje.data + "</div>";
            }
            gi("chatArea").scrollTop = gi("chatArea").scrollHeight;
        break;
    }
}

function enviar(){
    if(gi("chatInput").value != ""){
        var d = {'src': id_cliente, 'dst': 0, 'type': "msg", 'data': gi("chatInput").value};
        var j = JSON.stringify(d);
        console.log(j);
        websocket.send(j);
        gi("chatInput").value = "";
    }
}

function init(){
    gi("chatInput").addEventListener("keyup", function(e){if (e.keyCode == 13) {enviar();}});
    gi("chatBotonEnviar").addEventListener("click",function(){enviar();});
}

window.addEventListener("load", init);