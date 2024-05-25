var conexion = new WebSocket("ws://10.22.234.19:9090");
conexion.onopen=function(){
    console.log("Conexión abierta");
    //Subscribirse al topico /image_topic
    var subscribeMsg = {
        op: 'subscribe',
        topic: '/image_topic/compressed'
    };
    conexion.send(JSON.stringify(subscribeMsg));
}
conexion.onerror=function(error){
    console.log(error);
}

conexion.onmessage = function(event) {
    var message = JSON.parse(event.data);
    // Maneja el mensaje recibido desde el tópico suscrito
    if(message.topic === '/image_topic/compressed' && message.msg && message.msg.data){
        console.log("Received image data");
        var imageData = 'data:image/jpeg;base64,' + arrayBufferToBase64(message.msg.data);
        document.getElementById('compressedImage').setAttribute('src', imageData);
    }  else{
        console.log("Unexpected message format or topic");
      }
};


conexion.onmessage=function(r){
    var o=JSON.parse(r.data);

    document.getElementById("respuesta").innerHTML= o.msg.format;
}

var b=document.getElementById("bEnviar");

b.onclick=function(){
    var m=document.getElementById("mensaje");
    conexion.send(m.vale);

    var p=document.createElement("p");
    p.innerHTML=m.value;
    document.getElementById("mensajesEnviados").appendChild(p);
    //m.value="";

    console.log("pulse");
}

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}