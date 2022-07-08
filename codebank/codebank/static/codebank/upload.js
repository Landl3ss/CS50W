document.addEventListener('DOMContentLoaded', () => {
    var te_python = document.getElementById("manual_entry");
    let editor_python = CodeMirror.fromTextArea(te_python, {
        mode: "python",
        lineNumbers: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        indentWithTabs: true,
        indentUnit: 4
    });

    document.getElementById('submit_button').addEventListener('click', () => {

        editor_python.toTextArea();

    })
});
    