var conexion = new WebSocket("ws://localhost:9090");
conexion.onopen=function(){
    console.log("Conexión abierta");
}
conexion.onerror=function(error){
    console.log(error);
}