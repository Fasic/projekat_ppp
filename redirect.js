<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script language="JavaScript">

    function redirect() {
        var getUrl = window.location;
        console.log(getUrl.host);
        window.location.href = "http://" + getUrl.host + "/prisustvo";
    }

$(document).ready(function(){
    setInterval("redirect()", 5000);
});

</script>