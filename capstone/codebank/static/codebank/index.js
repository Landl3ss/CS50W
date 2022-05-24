document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('code_editor').style.display = 'none';
    document.getElementById('edit_button_div').style.display = 'block';
    document.getElementById('edit_buttons').style.display = 'none';

    document.getElementById('edit_button').addEventListener('click', () => {

        document.getElementById('code_editor').style.display = 'block';
        document.getElementById('edit_button_div').style.display = 'none';
        document.getElementById('edit_buttons').style.display = 'block';

        var te_python = document.getElementById("code");
        let editor_python = CodeMirror.fromTextArea(te_python, {
            mode: "python",
            lineNumbers: true,
            extraKeys: {"Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); }},
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            indentWithTabs: true,
            indentUnit: 4
        });

        document.querySelector('#save_button').addEventListener('click', () => {
            editor_python.save();
            editor_python.toTextArea();
            // editor_python.getTextArea();

            document.getElementById('code_editor').style.display = 'block';
            document.getElementById('edit_button_div').style.display = 'block';
            document.getElementById('edit_buttons').style.display = 'none';

            // var sb = document.getElementById("save_edit");
            // sb.click();
            
        })

    })
});
    