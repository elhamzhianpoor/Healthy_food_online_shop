// function show_hide() {
//     var x = document.getElementById("reply_form");
//     if (x.style.display === "none") {
//         x.style.display = "block";
//     } else {
//         x.style.display = "none";
//     }
// }

//
// function onchange_var() {
// let var_form = document.getElementById(var_form)
//     var_form.submit()
// }

function product_like(product_id,product_like_url,login_url){
    $.ajax({
        url:product_like_url,
        type:'get',
        data:{
           'product_id':product_id
        },
        success:function (data){
             if (data['login_required']) {
                window.location.href = login_url
            }
            let like_btn = document.getElementById('p_like')
            if (data['p_liked']) {
                like_btn.classList.remove('fa-regular')
                like_btn.classList.add('fa-solid')
            } else {
                like_btn.classList.remove('fa-solid')
                like_btn.classList.add('fa-regular')
            }
            let liker_c = document.getElementById('p_liker_count')
            liker_c.innerText = data['p_liker_count']

        }
    })

}



function like_comment(comment_id, like_url, login_url) {
    // event.preventDefault()
    $.ajax({
        url: like_url,
        type: 'get',
        data: {
            "com_id": comment_id
        },
        success: function (data) {
            if (data['login_required']) {
                window.location.href = login_url
            }
            let com_like_btn = document.getElementById('com_like'+comment_id)
            let com_dislike_btn = document.getElementById('com_dislike'+comment_id)

            if (data['liked']) {
                com_like_btn.classList.remove('fa-regular')
                com_like_btn.classList.add('fa-solid')
                com_like_btn.classList.add('text-primary')
                com_dislike_btn.classList.remove('fa-solid')
                com_dislike_btn.classList.add('fa-regular')
                // com_dislike_btn.classList.add('text-primary')

            } else {
                com_like_btn.classList.remove('fa-solid')
                com_like_btn.classList.add('fa-regular')
            }


            let liker_count = document.getElementById('like_counter')
            liker_count.innerText = data['like_counter']
            let dislike_count = document.getElementById('dislike_counter')
            dislike_count.innerText = data['dislike_counter']

        }

    })
}

function dislike_comment(comment_id, like_url, login_url) {
    $.ajax({
        url: like_url,
        type: 'get',
        data: {
            "com_id": comment_id
        },
        success: function (data) {
            if (data['login_required']) {
                window.location.href = login_url
            }
            let com_like_btn = document.getElementById('com_like'+comment_id)
            let com_dislike_btn = document.getElementById('com_dislike'+comment_id)
            if (data['disliked']) {
                com_dislike_btn.classList.remove('fa-regular')
                com_dislike_btn.classList.add('fa-solid')
                com_dislike_btn.classList.add('text-primary')
                com_like_btn.classList.remove('fa-solid')
                com_like_btn.classList.add('fa-regular')
                // com_like_btn.classList.add('text-primary')


            } else {
                com_dislike_btn.classList.remove('fa-solid')
                com_dislike_btn.classList.add('fa-regular')
            }
            let liker_count = document.getElementById('like_counter')
            liker_count.innerText = data['like_counter']
            let dislike_count = document.getElementById('dislike_counter')
            dislike_count.innerText = data['dislike_counter']


        }

    })
}