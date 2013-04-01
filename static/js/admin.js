$(document).ready(function(){
	var editor = ace.edit("post-content");
	editor.setTheme("ace/theme/textmate");
	editor.getSession().setMode("ace/mode/markdown");
	editor.getSession().setUseWrapMode(true);
	editor.renderer.setShowGutter(true);
	editor.setShowPrintMargin(false);
	editor.setFontSize(16);
	window.editor = editor;
});