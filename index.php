<!doctype html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <title> Trabajo de Grado de Daniel Rueda </title>

        <style>
            body {background-color: #b3ffb3; text-align:center;}
            form {width: 100%; max-width: 600px; margin: 0 auto; display: flex; flex-direction: column; justify-content: center; align-items: center;}
            
        </style>

    </head>

    <body>
    <div id="contenedor">
    <font face="Arial" >
    <form method="post" >
        <br>
        <b><font face="Arial, Helvetica, sans-serif"> Trabajo de Grado de Daniel Rueda </font></b><font face="Arial, Helvetica, sans-serif"><br>
        <br>
        <b><font face="Arial, Helvetica, sans-serif"> Login de Sistema </font></b><font face="Arial, Helvetica, sans-serif"><br>
        <br>
        <br>
        Usuario:  
        <INPUT TYPE="text" NAME="user" value=""><br><br>
        <br>
        Password:  
        <INPUT TYPE="password" NAME="password" value=""><br><br>
        <br>
        <INPUT TYPE="submit" NAME="btnConsultarLogin" value="Iniciar Sesion">
        <INPUT TYPE="reset" value="Limpiar los datos ">
        <br>
        <br>
        <br>
    </form>
    </div>
    </body>

</html>


<?php
if(isset($_POST['btnConsultarLogin'])){
//session_start();      printf($nombre);

    $nombre = $_POST['user'];
    $password = $_POST['password'];

    // DATOS DE CONEXION A LA BASE DE DATOS
    $servidor = "localhost";
    $usuario = "pi";
    $pass = "controlca";
    $db = "alarma";

    // REALIZANDO LA CONEXION A LA BASE DE DATOS
    $conexion = new mysqli($servidor, $usuario, $pass, $db);

    // VREIFICA LA CONEXION A LA BASE DE DATOS SINO LANZA UN ERRROR
    if (mysqli_connect_errno()) {
        printf("Conexión fallida: %s\n", mysqli_connect_error());
        exit();
    }

    // REALIZA LA CONSULTA A LA BASE  DE DATOS FILTRADO POR EL USUARIO Y PASS
    $consulta = mysqli_query ($conexion, "SELECT * FROM sesion WHERE user = '$nombre' AND pass = '$password'");  

  
    // SE VALIDA SI SE OBTIENE LOS RESULTADOS CON MYSQLI_FETCH_ASSOC
    // SI NO HAY RESULTADOS DEVOLVERÁ NULL QUE SE CONVERTIRA A BOLEANO PARA SER EVALUADO EN EL IF
    if($user = mysqli_fetch_assoc($consulta)) {
    
        //printf("EL USUARIO Y LA PWD SON CORRECTAS");
        // SE USA PARA CARGAR LA PAGINA DE REPORTE CUANDO ES VALIDO EL USUARIO Y PASS
        Header("Location: reportes.php");

    } else {
        // EMITE UN MENSAJE CUANDO UN USUARIO O PASSWORD ES INCORRECTO O NO EXISTE
        printf("EL USUARIO o EL PASSWORD NO EXISTE");

        exit();
    }
     
    //LIBERA LA MEMORIA 
    mysqli_free_result($consulta);
}

?>
