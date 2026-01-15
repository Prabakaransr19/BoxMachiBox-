const https = require('https');

function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    console.error("Parse Error for URL:", url, "Data:", data.substring(0, 100));
                    reject(e);
                }
            });
        }).on('error', (err) => reject(err));
    });
}

async function test() {
    try {
        console.log("Fetching sessions 2024...");
        const sessions = await fetchUrl("https://api.openf1.org/v1/sessions?year=2024&session_type=Race");
        const lastSession = sessions[sessions.length - 1];
        console.log("Last Session Key:", lastSession.session_key);

        console.log("Fetching Drivers...");
        const drivers = await fetchUrl(`https://api.openf1.org/v1/drivers?session_key=${lastSession.session_key}`);
        console.log("Drivers count:", drivers.length);

        console.log("Fetching Championship...");
        const champ = await fetchUrl(`https://api.openf1.org/v1/championship_drivers?session_key=${lastSession.session_key}`);
        console.log("Champ count:", champ.length);

    } catch (e) {
        console.error("Error:", e);
    }
}

test();
