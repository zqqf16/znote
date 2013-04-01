$(document).ready(function(){
	

});

!function ($) {
	var tools = '[data-toggle="tools"] tr'
	$(document).on('mouseover.tools', tools, function(e){
		var $this = $(this);
		$this.find(".tools-bar").show();
	})
	$(document).on('mouseout.tools', tools, function(e){
		var $this = $(this);
		$this.find(".tools-bar").hide();
	})
}(window.jQuery)