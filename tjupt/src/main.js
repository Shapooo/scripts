const completed_seeds_url = 'https://tjupt.org/torrents.php?inclbookmarked=0&incldead=0&picktype=0&keepseed=0&spstate=0&search_area=9&page='
const download_url = 'https://tjupt.org/download.php?id='

async function f() {
    const zip = new JSZip();
    let folder = zip.folder('torrents')
    let sum = 0
    for (let i = 0; ; ++i) {
        const items = await one_page(i)
        if (items.length == 0) {
            break
        }
        const ids = items.map((e) => e.innerHTML).filter((html) => html.indexOf('已下载，正在做种') == -1).map(text2id)
        console.log('get ', ids.length, ' valid ids, start to save')
        sum += ids.length
        for (const id of ids) {
            await save_torrent(id, folder)
            setTimeout(() => {

            }, 1000);
        }
    }

    console.log('get ', sum, 'torrent in total. compressing and saving...')
    zip.generateAsync({ type: 'blob' }).then(function (content) { saveAs(content, 'torrent.zip') })
}

async function save_torrent(id, zip_folder) {
    const url = download_url + id
    const res = await fetch(url)
    let file_name = res.headers.get('content-disposition')
    file_name = file_name.split('filename*=utf-8\'\'')[1]
    file_name = id + '-' + decodeURIComponent(file_name)
    console.log(file_name)
    const blob = await res.blob()
    zip_folder.file(file_name, blob, { base64: true })
}

async function one_page(page) {
    const completed_seeds_page_text = await (await fetch(completed_seeds_url + page)).text()
    const parser = new DOMParser
    const completed_seeds_doc = parser.parseFromString(completed_seeds_page_text, 'text/html')
    return Array.from(completed_seeds_doc.querySelectorAll('.torrentname'))
}


function text2id(text) {
    const start_idx = text.indexOf('a href="download.php?id=')
    const end_idx = text.indexOf('"><img')
    return parseInt(text.slice(start_idx + 24, end_idx), 10)
}

await f()