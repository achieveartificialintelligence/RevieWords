<?php
	header("Content-type:text/html;charset=utf-8");
	echo "<title>学习进度</title>";
	echo '<meta http-equiv="refresh" content="30">';
	echo '<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport">';
	
	$servername = "";
	$username = "";
	$password = "";
	$dbname = "";
	// 创建连接
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
		die("连接失败: " . $conn->connect_error);
	}
	
	if($_POST["fid"]!=""){
		$sql = 'DELETE FROM richeng WHERE id='.$_POST["fid"].';';
		$result = $conn->query($sql);
		echo "完成事件删除，请勿刷新！";
	}
	
	if($_POST["New_ShiJian"]!=""){
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(0,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+0 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(1,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+0 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(2,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+1 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(3,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+2 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(4,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+4 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(5,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+8 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(6,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+16 day")) . "');";
		$result = $conn->query($sql);
		$sql = "INSERT INTO `richeng`(`cishu`,`shijian`,`riqi`) VALUES(7,'" . $_POST["New_ShiJian"] . "','" . date("Ymd",strtotime("+32 day")) . "');";
		$result = $conn->query($sql);
		
		echo "完成事件新增，请勿刷新！";
	}
	
    echo 
    '	<form action="sun.php" method="post">
			<input type="text" name="New_ShiJian">
            <input type="submit" value="新增事项">
    	</form>
    	<br />
    ';
	
	
	$sql = "SELECT cishu, shijian, riqi, id FROM richeng ORDER BY riqi, cishu, shijian ASC";
	$result = $conn->query($sql);
	
	if ($result->num_rows > 0) {
		// 输出数据
		while($row = $result->fetch_assoc()) {
			if (date("Ymd")==$row["riqi"]){
                echo 
                '	<form action="sun.php" method="post">
	                	<p>第 <b  style="color:red;">' . $row["cishu"]. '</b> 次<br />
	                	<b  style="color:blue;">'. $row["shijian"]. '</b></p>
		                <input type="submit" name="fid" value="'.$row["id"].'">
	            	</form>
	            	<br />
	            ';
			}
		}
	} else {
		echo "空表";
	}
	
	$conn->close();
?>