!function ($) {
	var list = '[action-type="list"]';
	$(document).on('click.list', list, function(e) {
		var $this = $(this)
		, target = $this.attr("event-target");
		$this.parent().find(".active").removeClass("active");
		$this.addClass("active");
		$(target).trigger('status-toggle', [$this.attr("list-status"), $this.attr("list-index")]);
	});

	$(document).on('dblclick.list', list, function(e) {
		var $this = $(this)
		, index = $this.attr("list-index")
		, url = "/admin/write?id=" + index;
		
		window.location.href = url;
	});

	var btns = '[action-type="btn"]';
	$(document).on('status-toggle', btns, function(e, status, id) {
		$(this).find('a').each(function(){
			var $this = $(this)
			, type = $(this).attr("visible-status");
			$this.data("article-id", id);
			if ((type == "all") || (type == status))
				$this.show();
			else
				$this.hide();
		});
	});

	var btn = '[action-type="btn"] a';
	$(document).on('click.btn', btn, function(e) {
		var $this = $(this);
	});

}(window.jQuery)
