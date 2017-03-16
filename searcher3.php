<?php
/* David Zuccaro 14/03/2017 */

    $c = 0;
    $location = "";
    if (isset($_GET['submit'])) 
    {
        $location = $_GET['location'];                
    }                              

    if (strlen($location) > 0)
    {
        echo $location;        
        
        $username = "root";
        $password = "happy1";
        $hostname = "localhost"; 

        //connection to the database
        $dbhandle = mysql_connect($hostname, $username, $password) or die("Unable to connect to MySQL");
        
        //select a database to work with
        $selected = mysql_select_db("ghcndata", $dbhandle) or die("Could not select ghcndata database.");
        
        //execute the SQL query and return records
        $result = mysql_query("SELECT field1, station_name FROM station WHERE station_name LIKE '%" . $location . "%';");
        
        $row_count = mysql_num_rows($result);
                
        if ($row_count > 50)
        {            
            header("Location: http://localhost/clim-data/searcher2.php?message=Please refine your search");
            exit;
        }       
    }
?>

<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en'>
    
	<head>		
        <meta http-equiv='Content-Type' content='text/html;charset=utf-8'/>
        <meta http-equiv='refresh' content='900'/>
        <link rel='stylesheet' type='text/css' href='searcher.css'/>
		<title>Search And Graph Climate Data</title>           		
	</head>	 
   
    <body>        
        <div id='header'>
            <h1 class='dz'>Graph Climate Data</h1>
        </div>
        <form action='searcher4.php' method='get'>
            <div id='wrapper'>
                <div id='outer1'>Location:</div>
                <div id='outer2'>     
                <?php
                    echo "<select>";
                    
                    //fetch tha data from the database
                    while ($row = mysql_fetch_array($result)) 
                    {
                        echo "<option value='" . $row{'field1'} . "'>" . $row{'station_name'} . "</option>";
                    }
                    echo "</select>";
                
                    //close the connection
                    mysql_close($dbhandle);
            
                ?>
                </div>
                <div id='outer3'>
                    <input type='submit' value='submit' name='submit'/>
                </div>
                <div id='footer'>
                </div>
            </div><!-- end #wrapper -->	
        </form>
    </body>
</html>
