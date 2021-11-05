<!doctype html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <!-- SE USA PARA RECARGAR LA PAGINA DE REPORTE AUTOMATICAMENTE  -->
        <META HTTP-EQUIV="REFRESH" CONTENT="300;URL=reportes.php">
        <meta name="viewport" content="width=device-width, user-scalable=no, intial-scale=1.0 , maximun-scale=1.0, minimun-scale=1.0 ">
        <title> Trabajo de Grado de Daniel Rueda </title>
        <h1 align = center style="color:Green;" > DATOS DE LOS SENSORES CRONOLOGICAMENTE </h1>
                         
    </head>
<?php
// DATOS DE CONEXION A LA BASE DE DATOS
$servidor = "localhost";
$usuario = "pi";
$password = "controlca";
$db = "alarma";

// REALIZANDO LA CONEXION A LA BASE DE DATOS
$conexion = new mysqli($servidor, $usuario, $password, $db);

// VERIFICA LA CONEXION A LA BASE DE DATOS SINO LANZA UN ERRROR
if (mysqli_connect_errno()) {
    printf("Conexión fallida: %s\n", mysqli_connect_error());
    exit();
}

// REALIZA LA CONSULTA A LA BASE DE DATOS
$sql1 = "SELECT fecha, descripcion FROM movimiento";
$sql2 = "SELECT fecha, descripcion FROM teclado";
$sql3 = "SELECT fecha, descripcion FROM puerta";

// RESULTADO DE LA CONSULTA A LA BASE DE DATOS
$result1 =$conexion->query($sql1);
$result2 =$conexion->query($sql2);
$result3 =$conexion->query($sql3);


// CINTILLO DE ETIQUETA
echo "<table width=100%>"
."<tr>\n"
    ."<th width=33%> <h2 > Sensor Infrarrojo </h2></th> \n"
    ."<th width=33%> <h2> Sensor Puerta </h2> </th>\n"
    ."<th width=33%> <h2> Sensor Teclado </h2> </th>\n"

."</tr>\n"
."</table>";


// DETERMINAR EL NÚMERO DE FILAS DEL RESULTADO 
if ($result1->num_rows>0)   {

                            echo "<table border = 1 BGCOLOR=#EOEOFS align = left width=33%>"
                                ."<tr>\n"
                                    ."<th>Fecha</th>\n"
                                    ."<th>Descripcion</th>\n"
                                ."</tr>\n";

                                #IMPRIME LAS TABLAS DE LA BASE DE DATOS
                                while($row = $result1->fetch_assoc())  {
                                                                        print"<tr align=center>";
                                                                        print"<td >".$row['fecha']."</td>";
                                                                        print"<td>".$row['descripcion']."</td>";
                                                                        print"</tr>";
                                                                    }
                            }
   
if ($result2->num_rows>0)   {
                            echo "<table border = 1 BGCOLOR=#EOEOFS align = right width=33%>"
                                ."<tr>\n"
                                    ."<th>Fecha</th>\n"
                                    ."<th>Descripcion</th>\n"
                                ."</tr>\n";

                                
                                while($row = $result2->fetch_assoc())  {
                                                                        print"<tr align=center>";
                                                                        print"<td>".$row['fecha']."</td>";
                                                                        print"<td>".$row['descripcion']."</td>";
                                                                        print"</tr>";
                                                                    }

                            }
   
if ($result3->num_rows>0)   {
                            echo "<table border = 1 BGCOLOR=#EOEOFS align = center width=33%>"
                                ."<tr>\n"
                                    ."<th>Fecha</th>\n"
                                    ."<th>Descripcion</th>\n"
                                ."</tr>\n";
    
                                
                                while($row = $result3->fetch_assoc())  {
                                                                        print"<tr align=center>";
                                                                        print"<td>".$row['fecha']."</td>";
                                                                        print"<td>".$row['descripcion']."</td>";
                                                                        print"</tr>";
                                                                    }
    
                                }

//LIBERA LA MEMORIA 
mysqli_free_result($result1);
mysqli_free_result($result2);
mysqli_free_result($result3);

/* CIERRA LA CONEXION A LA BASE DE DATOS */
$conexion->close();                          
?>

<body BGCOLOR = #FFFFFF font-family = Arial>
</body>
</html>
