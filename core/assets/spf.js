let pages = SPF_PAGES;

page_contents = {};

for (let i = 0; i < pages.length; i++) {
    page_info = await fetch(pages[i]);
    page_info = await page_info.json();
    page_contents[page_info.title] = {
        "title": page_info.title,
        "content": page_info.content
    }
}

// get current page from url #hash
let current_page = window.location.hash;
current_page = current_page.replace("#", "");

// if current page is not in page_contents, set it to the first page
if (page_contents[current_page] == undefined) {
    current_page = pages[0];
}

// set the page title
document.title = page_contents[current_page].title;

// set the page content
document.getElementById("content").innerHTML = page_contents[current_page].content;
