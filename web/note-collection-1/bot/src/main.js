const mysql = require('mysql');
const puppeteer = require( 'puppeteer' );

const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
const databaseNames = process.env.DB_NAMES.split(",")

const connectToDatabase = async () => {
    console.log("[ ] Connecting to database...")
    const conn = mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD
    });

    let connected = false
    while(!connected)
    {
        await delay(1500);
        conn.connect((err) => {
            if (err){ 
                console.log(err);
            } else {
                connected = true
            }
        });
    }
    console.log("[OK] Connection to database established!")
    return conn
}

const getPassword = (chal) => {
    return {
        'chal01': '398pyhrdnmfk1398yeglbfn13y4vlbenro127tf3vewbsl',
        'chal02': 'i389ygiwheojfkn13p7r9hudbfvo136l8r,fetcr',
        'chal03': '011k2098h19z2no913g79g3z192319n2xo123gl1273m12',
        'chal04': 'mdjf913hbne8y7t16f3tv8rioy13gvb9137t1f3i78319h',
        'chal05': '254yfi382479utfbnp93274urvjfdsio87gy'
    }[chal]
}

const getUrl = (chal) => {
    return {
        'chal01': 'https://note-collection-1.wep.dk',
        'chal02': 'https://note-collection-2.wep.dk',
        'chal03': 'https://note-collection-3.wep.dk',
        'chal04': 'https://note-collection-4.wep.dk',
        'chal05': 'https://note-collection-5.wep.dk'
    }[chal]
}

const showLog = (note_id, msg) => {
    const time = (new Date()).toLocaleTimeString().replaceAll(".", ":")
    console.log(`[${time}] [${note_id}] ${msg}`)
}

const filterRequestLog = (request, callback) => {
    const url = request.url()
    const ignore = [
        'https://cdnjs.cloudflare.com/ajax/libs/uikit/2.27.5/fonts/fontawesome-webfont.woff2',
        'https://cdnjs.cloudflare.com/ajax/libs/uikit/2.27.5/css/uikit.min.css',
        'https://note-collection-2.wep.dk/assets/css/',
    ]
    for(let i = 0; i < ignore.length; i++){
        if(url.includes(ignore[i])){
            request.abort();
            return;
        }
    }

    request.continue()
    callback()
}

const launchBot = async (challenge, note_id) => {
    const base_url = getUrl(challenge)
    let browser = null;
    try
    {
        showLog(note_id, `Launching browser for challenge ${challenge}`)
        browser = await puppeteer.launch({
            "args": [
            "--no-sandbox"
            ]});
        const page = await browser.newPage();
        page.setDefaultTimeout(3000); 
        page.setDefaultNavigationTimeout(3000); 
        
        await page.setRequestInterception(true);
        page.on('request', request => 
            filterRequestLog(
                request, () => 
                    showLog(note_id, `Requesting ${request.method()} ${request.url()}`)
                ));

        page.on('requestfailed', request => {
            if (request.isInterceptResolutionHandled()) return;
            showLog(note_id, `Request FAILED for '${request.method()} ${request.url()}': ${request.failure().errorText}`)
        });
                 
        page.on('requestfinished', request => {
            const response = request.response()
            const isRedirect = response.status() >= 300 && response.status() < 400;

            if(isRedirect){
                showLog(note_id, `Got redirect '${response.status()} ${response.headers()["location"]}' for ${request.method()} ${request.url()}`)
            } else {
                showLog(note_id, `Got response '${response.status()} ${response.statusText()}' for ${request.method()} ${request.url()}`)
            }
        });

        await page.goto(base_url + '/login.php');
        await page.waitForSelector("input[name=username]");
        await page.type('input[name=username]', 'admin');
        await page.type('input[name=password]', getPassword(challenge));
        await page.click("#btn-login");

        await page.waitForSelector('h1')
        const logoutLink = await page.$('a[href="/logout.php"]')
        const alert = await page.$('div.uk-alert')

        if(alert){
            const message = await page.evaluate(el => el.textContent, alert)
            showLog(note_id, `Alert message: ${message}`)
        }

        if(!logoutLink){
            showLog(note_id, "Failed to authenticate as admin!")
            if(browser)
                await browser.close();
        }

        await page.goto(base_url + '/view.php?note=' + note_id, {
            waitUntil: ['load','networkidle2'],
        });
        showLog(note_id, "Finished viewing note")

        await browser.close();
    } catch(e){
        console.log("Error: ", e)
        
        if (e instanceof puppeteer.errors.TimeoutError) {
            showLog(note_id, "Got timeout")
            await browser.close();
            return;
        }
        throw e;
    }
}

const blockBot = async (conn, database, node_id) => {
    conn.query(`UPDATE ${database}.notes SET is_blocked=1 WHERE is_blocked=0 AND id=?`, node_id, function (err, rows, fields) {
        if (err) throw err;
    })
}

const main = async () => {
    const conn = await connectToDatabase()
    while(true)
    {
        databaseNames.forEach(database => {
            conn.query(`SELECT id FROM ${database}.notes WHERE is_blocked=0 AND reported IS NOT NULL`, function (err, rows, fields) {
                if (err) throw err;

                rows.forEach(async (row) => {
                    console.log(new Date(), "Received reported note: ", row.id)
                    await blockBot(conn, database, row.id)
                    await launchBot(database, row.id)
                })
            });
        });
        await delay(15000)
    }
}

(async () => await main())()