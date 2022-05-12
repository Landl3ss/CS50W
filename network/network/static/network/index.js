document.addEventListener('DOMContentLoaded', function() {

    let submit_button = document.querySelector('#index_submitbutton');
    if(submit_button !== null) {
        submit_button.disabled = true;
        document.querySelector('#index_speech').onkeyup = () => {
            if(document.querySelector('#index_speech').value.length > 0) {
                submit_button.disabled = false;
            } else {
                submit_button.disabled = true;
            }
        }
    }


    document.querySelectorAll('.edit_post').forEach(edit => edit.onclick = function() {
        let post_div_id = edit.parentElement.parentElement.id;
        // alert(post_div_id);
        let subject = edit.parentElement.parentElement.querySelector('.subject').textContent;
        edits(post_div_id, subject);
    })
    

    document.querySelectorAll('.heart_button').forEach(heart => {
        let pid = heart.parentElement.parentElement.id;
        let e = heart.parentElement.querySelector('.likes');
        
        fetch(`/likeit/${pid}`, {method: 'GET'})
        .then(response => response.json())
        .then(h => {
            // console.log(e);
            if(h['exist'] === true){
                if(h['like'] === true) {
                    heart.innerHTML = '❤️';
                    e.innerHTML = `${h['likes']} Likes`;
                } else if(h['like'] === false) {
                    heart.innerHTML = '♡';
                    e.innerHTML = `${h['likes']} Likes`;
                }
            } else if(h['exist'] === false) {
                e.innerHTML = `${h['likes']} Likes`;
            }
        })
    })


    document.querySelectorAll('.heart_button').forEach(heart => heart.onclick = function() {
        let pid = heart.parentElement.parentElement.id;
        let e =heart.parentElement.querySelector('.likes');
        let num = parseInt(heart.parentElement.querySelector('.likes').innerHTML);


        if(heart.innerHTML === '♡') {
            heart.innerHTML = '❤️';
            e.innerHTML = `${num + 1} Likes`;
            likeit(pid, true);
        } else if(heart.innerHTML === '❤️') {
            heart.innerHTML = '♡';
            e.innerHTML = `${num - 1} Likes`;
            likeit(pid, false);
        }
    })
})


function edits(postid, subject) {
    // alert('hello');
    let subject_div = document.getElementById(postid).querySelector('.subject_div');
    let edit_textarea = document.createElement('textarea');

    let paragraph = subject_div.childNodes[1];
    // alert(paragraph);
    edit_textarea.innerHTML = subject;
    subject_div.replaceChild(edit_textarea, paragraph);

    let edit_button = document.createElement('button');
    edit_button.setAttribute('class', 'btn btn-secondary');
    edit_button.innerHTML = "Save!";
    subject_div.appendChild(edit_button);

    edit_button.addEventListener('click', function() {
        if(subject != edit_textarea.value) {
            fetch(`/edit_post/${postid}`, {
                method:"PUT",
                body: JSON.stringify({
                    speech: edit_textarea.value
                })
            })
        }
        location.reload();
    })
}


function likeit(pid, torf) {
    fetch(`/likeit/${pid}`, {
        method: 'PUT',
        body:JSON.stringify({
            like: torf
        })
    })
}