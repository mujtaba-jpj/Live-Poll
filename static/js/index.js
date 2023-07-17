let selectedLink = document.querySelector(".selectedLink");

function checkActive() {
    document.querySelectorAll("nav li").forEach((item) => {
        console.log(item);
        if (item.dataset.active == "true") {
            selectedLink.style.transform = `translateX(${item.offsetLeft + item.offsetWidth / 2 - 24 + "px"
                })`;
        }
    });
}

document.querySelectorAll("nav li").forEach((item) => {
    console.log(item.offsetLeft);
    item.addEventListener("click", (e) => {
        document.querySelectorAll("nav li").forEach((i) => {
            i.dataset.active = "false";
        });
        e.currentTarget.dataset.active = "true";
        checkActive();
    });
});

checkActive();
