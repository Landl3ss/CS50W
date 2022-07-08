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
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            indentWithTabs: true,
            indentUnit: 4
        });

        document.querySelector('#cancel_button').addEventListener('click', () => {
            let filename = document.getElementById('filename_location').innerHTML;
            fetch(`file_redirect/${filename}`)
        });

    })
}); 