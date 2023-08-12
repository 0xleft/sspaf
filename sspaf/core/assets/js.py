page = """
let pages = SSPAF_PAGES;

page_contents = {};

for (let i = 0; i < pages.length; i++) {
    fetch(pages[i]).then(response => response.json().then(data => {
        page_contents[data.title] = {
            "title": data.title,
            "content": data.content
        }
    }));
}

setTimeout(() => {
    updateContent();
}, 200);

window.addEventListener("hashchange", updateContent);

function updateContent() {
    let current_page = window.location.hash;
    console.log(current_page);
    current_page = current_page.replace("#", "");

    if (page_contents[current_page] != undefined) {
        let scripts = document.getElementsByClassName("sspaf-script");
        for (let i = 0; i < scripts.length; i++) {
            scripts[i].remove();
        };
        document.title = page_contents[current_page].title;
        document.getElementById("content").innerHTML = page_contents[current_page].content;
    };
};

function loadScript(url) {
    let script = document.createElement("script");
    script.src = url;
    script.className = "sspaf-script";
    document.head.appendChild(script);
}
"""