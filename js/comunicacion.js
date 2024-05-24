var conexion = new WebSocket("ws://localhost:9090");
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
};

conexion.onmessage=function(r){
    var o=JSON.parse(r.data);


    document.getElementById("respuesta").innerHTML=o.msg.data;
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