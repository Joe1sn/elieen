<?php

include 'flag.php';
highlight_file("index.php");




$str = $_GET['str'];


if(substr(md5($str), 0,6) == 'e10adc' && $str > 100)
{
	echo"true!";
	require_once'flag.php';
	echo"<br>";
	echo $flag;
}
else{
	echo"no! try again!";
}


?>