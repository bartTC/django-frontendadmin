<script src="http://jqueryjs.googlecode.com/files/jquery-1.2.6.min.js" type="text/javascript"></script>
<script type="text/javascript">
jQuery(document).ready(function(){
	$('a.frontendadmin').each(function(){
		$(this).click(function(){
			$(this).parent().load($(this).attr('href'));
			return false;
		});
	})
});
</script>
