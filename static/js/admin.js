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

	var query = '[data-toggle="query"] a';
	$(document).on('click.query', query, function(e){
		var $this = $(this)
		, value = $this.attr("href")
		, type = $this.attr("data-query");
		window.location.href = get_query_url(type, value);
		return false;
	})
}(window.jQuery)