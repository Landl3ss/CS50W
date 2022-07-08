document.addEventListener('DOMContentLoaded', function() {

    let answer = document.getElementById("answer");

    


    (function loop() {

        setTimeout(function () {
            location.reload();
            fetch('/get_price',
                {
                    method: 'POST'
                })
            location.reload();
            loop()
        }, 60000);
    }());
})

// function get_price() {
//     fetch('/get_price', {
//         method: 'POST'
//     })
//         .then(response => response.json())
//         .then(result => {
//             if (result === 0) {
//                 location.reload();
//             }
//         })
// }

