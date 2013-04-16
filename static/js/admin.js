!function ($) {
	$doc = $(document);
	var list = '[action-type="list"]';
	$doc.on('click.list', list, function(e) {
		var $this = $(this)
		, target = $this.attr("event-target");
		$this.parent().find(".active").removeClass("active");
		$this.addClass("active");
		$(target).find("a").trigger('status-toggle', [$this.attr("list-status"), $this.attr("list-index")]);
	});

	$doc.on('dblclick.list', list, function(e) {
		var $this = $(this)
		, index = $this.attr("list-index")
		, url = "/admin/write?id=" + index;
		
		window.location.href = url;
	});

	var btn = '[action-type="btn"] a';
	$doc.on('status-toggle', btn, function(e, status, id) {
		var $this = $(this)
		, visible = $this.attr("visible-status") ;

		if ((visible == status) || (visible == "all")) {
			$this.data("article-id", id);
			$this.show();
		} else {
			$this.hide();
		}
	});

	$doc.on('click.btn', btn, function(e) {
		var $this = $(this)
		, id = $this.attr("id")
		, if_status = false;
		
		switch(id) {
			case "btn-published": 
			case "btn-no-page": if_status="published"; break;
			case "btn-draft": if_status="draft"; break;
			case "btn-delete": if_status="delete"; break;
			case "btn-page": if_status="page"; break;
			case "btn-edit": 
				window.location.href="/admin/write?id="+$this.data("article-id");
				break;
			case "btn-write":
				window.location.href="/admin/write";
				break;
		}
		if (if_status) {
			$.post('/admin/article',
					{"action": if_status, "id": $this.data("article-id")},
					function(e) {
						if (e.status == 0) {
							window.location.reload();
						} else {
							$doc.trigger("znote.alert", ['error', e.msg]);
						}
					}
			);
		}
	});

}(window.jQuery)

!function($) {
	$doc = $(document);

	var action_event = '[action-type="event"]';

	$doc.on("click.event", action_event, function(){
		var type = $(this).attr("event-type");
		$doc.trigger(type);
	});

	var save = function(type) {
		var $ctg = $("#category")
		, $url = $("#url")
		, $id = $("#id");

		$.post("/admin/write", 
				{"title": $("#title").val(),   "content": window.editor.getValue(),
				 "category": $ctg.data("val"), "slug": $url.data("val"),
				 "id": $id.val(),              "status": type,
				},
				function(e) {
					if (e.status == 0) {
						$id.val(e.article.id);
						$doc.trigger("znote.alert", ['success', '操作成功']);
					} else {
						$doc.trigger("znote.alert", ['error', e.msg]);
					}
				}
		);
	};

	$doc.on('znote.write.published', function(e) {
		save("published");
	});
	$doc.on('znote.write.draft', function(e) {
		save("draft");
	});
	$doc.on('znote.write.page', function(e) {
		save("page");
	});

}(window.jQuery)

!function($) {
	var get_alert = function(e, type, msg) {
		return '<div id="alert" class="alert alert-' + type
		   + ' span8 offset2"><a class="close" data-dismiss="alert">×</a>' 
		   + msg + '</div>';
	}

	$(document).on('znote.alert', function(type, title, msg){
		var $info = $("#info-bar");
		$info.html(get_alert(type, title, msg));
	});

}(window.jQuery)
