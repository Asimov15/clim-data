<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en'>
    
	<head>		
        <meta http-equiv='Content-Type' content='text/html;charset=utf-8'/>
        <meta http-equiv='refresh' content='900'/>
        <link rel='stylesheet' type='text/css' href='global.css'/>
        <link rel='stylesheet' type='text/css' href='searcher4.css'/>    
        <link rel='shortcut icon' href='Dapino-Summer-Holiday-Sun.ico' type='image/x-icon'>
		<title>Search And Graph Climate Data</title>           		
	</head>	
    <?php 
        function RandomString()
        {
            $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            $randstring = '';
            for ($i = 0; $i < 10; $i++) 
            {
                $randstring = $randstring . $characters[rand(0, strlen($characters) - 1)];
            };

            return $randstring;
        };			
        $outfn = RandomString() . ".png"; 
        
        $station_id = 'ASN00031037';  #default
        if (isset($_GET["submit"])) 
        {
            if (strlen($_GET['station_id']) > 0)
            {
                $station_id = $_GET['station_id'];
            }            
            else
            {
                echo "Failed to get station id\n";
            }
        }        
        
        $cmd = '/usr/bin/python clim-av.py -f ' . $outfn . ' -s ' . $station_id;
        
        exec($cmd, $a);        
        
        echo "<body>";        
                //    <div id='header'>
                  //      <h1 class='dz'>Graph Climate Data</h1>
                   // </div>";                    
        echo "          <img class='dz' alt='Climate Data' width='1870px' src='images/" . $outfn . "'/>";                
    ?> 
    
    <a class='search' href='searcher2.php'>Search Again</a>
    
    </body>
    
</html>
