<?php
/* David Zuccaro 14/03/2017 */

    $c = 0;
    $location = "GEELONG";  //default
    
    if (isset($_GET['submit'])) 
    {
        $location = $_GET['location'];                
    }                              

    if (strlen($location) > 0)
    {
        $username = "root";
        $password = "happy1";
        $hostname = "localhost"; 

        //connection to the database
        $dbhandle = mysql_connect($hostname, $username, $password) or die("Unable to connect to MySQL");
        
        //select a database to work with
        $selected = mysql_select_db("ghcndata", $dbhandle) or die("Could not select ghcndata database.");
        
        //execute the SQL query and return records
        $cmd = "SELECT station.field1, station.station_name, country.code, country.name FROM station INNER join country ON station.country_code = country.code WHERE station_name LIKE '%" . $location . "%' AND temperatures = 1;";
 
        $result = mysql_query($cmd);
        
        $row_count = mysql_num_rows($result);
                
        if ($row_count > 50)
        {            
            header("Location: http://localhost/clim-data/searcher2.php?message=Please refine your search");
            exit;
        }
        if ($row_count <= 0)
        {            
            header("Location: http://localhost/clim-data/searcher2.php?message=No matching stations found");
            exit;
        }
    }
?>

<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en'>
    
	<head>		
        <meta http-equiv='Content-Type' content='text/html;charset=utf-8'/>
        <meta http-equiv='refresh' content='900'/>
        <link rel='stylesheet' type='text/css' href='global.css'/>
        <link rel='stylesheet' type='text/css' href='searcher3.css'/>        
		<title>Search And Graph Climate Data</title>        
	</head>	 
   
    <body>        
        <div id='header'>
            <h1 class='dz'>Graph Climate Data</h1>
        </div>
         <div id='message'>
             &nbsp;        
        </div>
        <form action='searcher4.php?' method='get'>
            <div id='wrapper'>
                <div id='outer1'>Location:</div>
                <div id='outer2'>     
                <?php
                    $spaces_to_add = 5;
                    $biggest_length = 0;
                    $row = array();
                    echo "<select name='station_id'>\n";
                    $x = 0;
                     //fetch tha data from the database
                    while ($row[$x] = mysql_fetch_array($result)) 
                    {                        
                        $row[$x]{'station_name'} = preg_replace('!\s+!', ' ', $row[$x]{'station_name'}); // remove duplicate spaces
                        if (strlen($row[$x]{'station_name'}) > $biggest_length)
                        {
                            $biggest_length = strlen($row[$x]{'station_name'});
                        };
                        $x = $x + 1;
                    };
                   
                    $y = 0;
                    for ($y = 0; $y < $x; $y++)
                    {
                        $z = $biggest_length - strlen(trim($row[$y]{'station_name'})) + $spaces_to_add;                                            
                        
                        $picker = trim($row[$y]{'station_name'}) . str_repeat('&nbsp;', $z) . $row[$y]{'name'};
                        echo "                      <option value='" . $row[$y]{'code'} . $row[$y]{'field1'} . "'>" . $picker . "</option>\n";
                    }
                    
                    echo "                  </select>\n";
                
                    //close the connection
                    mysql_close($dbhandle);            
                ?>
                </div>
            
                <div id='outer3'>  
                    (Select Weather Station)
                </div>
                <div id='outer4'>
                    <input class='button' type='submit' value='submit' name='submit'/>
                </div>                
            </div><!-- end #wrapper -->	
                        
        </form>
        <a class='search' href='searcher2.php'>Search Again</a>
    </body>
</html>
