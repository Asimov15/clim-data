<?php
/* David Zuccaro 14/03/2017 */
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
        <br/>
        <div id='message'>
        <?php
            if (isset($_GET['message'])) 
            {
                echo $_GET['message'];
            }
            else
            {
                // Fallback behaviour goes here
            }
        ?>
        </div>
        <form action='searcher3.php' method='get'>
            <div id='wrapper'>
                <div id='outer1'>Location:</div>
                <div id='outer2'>
                    <input name='location' value='' type='text'/>
                </div>
                <div id='outer3'>                    
                    <input type='submit' value='submit' name='submit'/> 
                </div>
                <div id='footer'>
                </div>
            </div>   <!-- end #wrapper -->	
        </form>
    </body>
</html>
