$(document).ready(function(){
	var editor = ace.edit("post-content");
	editor.setTheme("ace/theme/textmate");
	editor.getSession().setMode("ace/mode/markdown");
	editor.getSession().setUseWrapMode(true);
	editor.getSession().setWrapLimitRange(80, 80);
	editor.renderer.setShowGutter(true);
	editor.setShowPrintMargin(false);
	window.editor = editor;
});