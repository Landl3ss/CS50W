document.addEventListener('DOMContentLoaded', function() {

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


function likeit(pid, torf) {
    fetch(`/likeit/${pid}`, {
        method: 'PUT',
        body:JSON.stringify({
            like: torf
        })
    })
}