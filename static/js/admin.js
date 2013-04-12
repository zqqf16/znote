!function ($) {
	var list = '[action-type="list"]';
	$(document).on('click.list', list, function(e) {
		var $this = $(this)
		, target = $this.attr("event-target");
		$this.parent().find(".active").removeClass("active");
		$this.addClass("active");
		$(target).find("a").trigger('status-toggle', [$this.attr("list-status"), $this.attr("list-index")]);
	});

	$(document).on('dblclick.list', list, function(e) {
		var $this = $(this)
		, index = $this.attr("list-index")
		, url = "/admin/write?id=" + index;
		
		window.location.href = url;
	});

	var btn = '[action-type="btn"] a';
	$(document).on('status-toggle', btn, function(e, status, id) {
		var $this = $(this)
		, visible = $this.attr("visible-status") ;

		if ((visible == status) || (visible == "all")) {
			$this.data("article-id", id);
			$this.show();
		} else {
			$this.hide();
		}
	});

	$(document).on('click.btn', btn, function(e) {
		var $this = $(this)
		, id = $this.attr("id")
		, if_status = false;
		
		switch(id) {
			case "btn-publish": 
			case "btn-unfix": if_status="publish"; break;
			case "btn-draft": if_status="draft"; break;
			case "btn-delete": if_status="delete"; break;
			case "btn-fix": if_status="fix"; break;
			case "btn-edit": 
				window.location.href="/admin/write?id="+$this.data("article-id");
				break;
		}
		if (if_status) {
			$.post('/admin/article',
					{"action": if_status, "id": $this.data("article-id")},
					function(e) {
						if (e.status == 0) {
							window.location.reload();
						} else {
							alert(e.msg);
						}
					}
			);
		}
	});

}(window.jQuery)
