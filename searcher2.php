<?php
/* David Zuccaro 14/03/2017 */
?>

<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en'>
    
	<head>		
        <meta http-equiv='Content-Type' content='text/html;charset=utf-8'/>
        <link rel='stylesheet' type='text/css' href='global.css'/>
        <link rel='stylesheet' type='text/css' href='searcher2.css'/>
        <link rel='shortcut icon' href='Dapino-Summer-Holiday-Sun.ico' type='image/x-icon'>
		<title>Search And Graph Climate Data</title>           		
	</head>	 
   
    <body>               
        <h1 class='dz'>Graph Climate Data</h1>
        
        <br/>
        <div id='message'>
        <?php
            if (isset($_GET['message'])) 
            {
                echo $_GET['message'];
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
                    Enter the first few characters of weather station.
                    <br/>
                    Good examples to try are:
                    <br/>
                    - Melbourne
                    <br/>
                    - Moscow
                    <br/>
                    - Amundsen
                    <br/>
                    - Cairns
                    <br/>
                </div>
                <div id='outer4'>                    
                    <input class='button' type='submit' value='Submit' name='submit'/> 
                </div>        
            </div>   <!-- end #wrapper -->	
        </form>
    </body>
</html>
