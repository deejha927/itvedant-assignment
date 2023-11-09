$(document).ready(function () {
    // Add a click event handler to all elements with class "toggle-button"
    $(".toggle-button").click(function () {
        // Get the target element ID from the "data-target" attribute
        const target = $(this).data("target");
        // Toggle the visibility of the target element with a slide animation
        $("#" + target).slideToggle();
        const action = $(this).data("action");
        if (action === "show") {
            $(this).text("Show Less Comments");
            $(this).data("action", "hide");
        } else {
            $(this).text("Show More Comments");
            $(this).data("action", "show");
        }
    });

});

function showOverLay(text, id) {
    var myForm = $("#form");
    myForm.attr("action", `/answer/${id}/`);
    $("#text").text(text);
    $("#overlay").css("display", "flex");
}
function hideOverLay() {
    $("#text").text("");
    $("#overlay").css("display", "none");
}
async function likeComment(id) {
    try {

        const div = $(`#like-${id}`);
        let count = parseInt(div.text());
        const apiUrl = `/like/${id}/`;
        const response = await fetch(apiUrl);
        if (response.status == 403) {
            const data = await response.json();
            return alert(data["message"]);
        };
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        count = data["liked"] ? count + 1 : count - 1;
        div.text(count);


    } catch (error) {
        console.error('Request failed:', error);
    }
}


async function deletePost(id) {
    try {
        const apiUrl = `/posts/${id}/`;
        const response = await fetch(apiUrl, { method: "DELETE" });
        if (response.status == 200) {
            console.log("here");
            $(`#post-${id}`).remove();
        } else {
            const data = await response.json();
            return alert(data["message"]);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

async function likePost(id) {
    try {
        const apiUrl = `/postslike/${id}/`;
        const response = await fetch(apiUrl);
        var icon = $(`#message-like-icon-${id}`);
        var count = $(`#message-like-${id}`);
        if (response.status == 200) {
            let likeCount = parseInt(count.text()) - 1;
            icon.html(`<i class="fa fa-heart-o text-xl text-red-500" aria-hidden="true" onclick="likePost(${id})"></i>`);
            count.html(likeCount);
        }
        else if (response.status == 201) {
            let likeCount = parseInt(count.text()) + 1;
            icon.html(`<i class="fa fa-heart text-xl text-red-500" aria-hidden="true" onclick="likePost(${id})"></i>`);
            count.html(likeCount);
        }
        else {
            console.log("something went wrong");
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}