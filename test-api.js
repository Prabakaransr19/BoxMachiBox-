const fetch = require('node-fetch'); // or global fetch if node 18+

async function test() {
    try {
        console.log("Fetching sessions...");
        const sessionRes = await fetch("https://api.openf1.org/v1/sessions?year=2024&session_type=Race"); // Using 2024 as 2025 likely empty
        const sessions = await sessionRes.json();

        if (sessions.length === 0) {
            console.log("No 2024 sessions found.");
            return;
        }

        const lastSession = sessions[sessions.length - 1]; // Last race
        console.log("Last Session Key:", lastSession.session_key, "Location:", lastSession.location);

        console.log("\nFetching Championship Drivers...");
        // Try the search result endpoint
        // Note: URL might need session_key
        const champRes = await fetch(`https://api.openf1.org/v1/championship_drivers`); // Try without key first to see if it lists all
        // If that fails or returns too much, filter
        // Actually prompt said `?session_key=latest`.
        // Let's try `current` endpoint logic.

        const sampleText = await champRes.text();
        try {
            const champ = JSON.parse(sampleText);
            console.log("Championship Drivers Record Count:", champ.length);
            if (champ.length > 0) console.log("Sample:", champ[0]);
        } catch (e) {
            console.log("Failed to parse champ drivers:", sampleText.slice(0, 100));
        }

        console.log("\nFetching Championship Teams...");
        // Guessing endpoint name based on logic
        const constRes = await fetch(`https://api.openf1.org/v1/championship_constructors`);
        const constText = await constRes.text();
        try {
            const consts = JSON.parse(constText);
            console.log("Championship Constructors Record Count:", consts.length);
            if (consts.length > 0) console.log("Sample:", consts[0]);
        } catch (e) {
            console.log("Failed to parse champ constructors:", constText.slice(0, 100));
        }

    } catch (e) {
        console.error("Error:", e);
    }
}

test();
