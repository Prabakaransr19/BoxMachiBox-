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
                    resolve([]);
                }
            });
        }).on('error', (err) => reject(err));
    });
}

async function testDriverHistory() {
    try {
        const driverNumber = 1; // Verstappen
        const year = 2024;

        console.log(`Fetching race history for driver ${driverNumber} in ${year}...`);

        // 1. Get all race sessions for the year
        const sessions = await fetchUrl(`https://api.openf1.org/v1/sessions?year=${year}&session_type=Race`);
        console.log(`Found ${sessions.length} races.`);

        if (sessions.length === 0) return;

        // 2. Fetch results for a few sessions to see structure
        // Endpoint: /position?session_key=...&driver_number=...
        // This gives lap-by-lap usually. We want FINAL position.
        // Actually, /position endpoint documentation says "Driver position throughout a session".
        // It might return one record per lap or per change.
        // We need the LAST record for the session.

        const lastSession = sessions[sessions.length - 1];
        console.log(`Checking Session ${lastSession.session_key} (${lastSession.location})...`);

        const positions = await fetchUrl(`https://api.openf1.org/v1/position?session_key=${lastSession.session_key}&driver_number=${driverNumber}`);
        console.log(`Position records: ${positions.length}`);
        if (positions.length > 0) {
            console.log("Last position record:", positions[positions.length - 1]);
        }

    } catch (e) {
        console.error(e);
    }
}

testDriverHistory();
