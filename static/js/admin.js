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

	var get_args = function() {
		var args = {}
		, query = window.location.search.substring(1);
    	var pairs = query.split("&");
    	for(var i=0;i<pairs.length;i++) {
        	var sign = pairs[i].indexOf("="); 
        	if(sign == -1) continue;
        	var key = pairs[i].substring(0,sign);
        	var value = pairs[i].substring(sign+1);       
        	args[key] = value;
    	}
    	return args;
	}

	var get_query_url = function(key, value) {
		var args = get_args()
		, url = '';
		args[key] = value;
		for (var k in args) {
			url += k + "=" + args[k] + '&'
		}

		return window.location.pathname + "?" + url.trim('&');
	}

	var edit = '[data-toggle="edit-inline"]';
	$(document).on('click.edit', edit, function(e){
		var $this = $(this)
		, $input = $($this.attr("href"));
		$this.addClass("hide");
		$input.removeClass("hide");
		$input.val($this.html());
		$input.focus();
		var fallback = function() {
			$this.removeClass("hide");
			$input.addClass("hide");
			$this.html($input.val());
		}
		$input.on('blur', function(e){
			fallback();
		});
		$input.on("keydown", function(e) {
			if (e.keyCode == 13) {
				fallback();
			}
		})
		return false;
	})

	var action = '[data-toggle="action"]';
	$(document).on('click.action', action, function(e){
		var $this = $(this)
		, title = $("#title").html()
		, content = window.editor.getValue()
		, $id = $("#id")
		, id = $id.val();

		alert(title);
		$.post("/admin/write", {title: title, content: content, id: id}, function(result){
			if (result.status == 0){
				$id.val(result.article.id)
			} else {
				alert("error")
			}
		})
	})
}(window.jQuery)
