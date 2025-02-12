const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.send(`
        <h1>Ping a Website</h1>
        <form method="POST" action="/ping">
            <label for="host">Enter a hostname or IP address:</label>
            <input type="text" id="host" name="host" placeholder="e.g., google.com">
            <button type="submit">Ping</button>
        </form>
    `);
});

app.post('/ping', (req, res) => {
    const host = req.body.host;

    //validate the input (allow aplhanumeric, dots, and hyphens)
    if(!/^[a-zA-Z0-9.-]+$/.test(host)) 
    {
        return res.status(400).send('Invalid hostname');
    }

    //secure code: use execfile with argumeents
    execFile(`ping`, ['-c','4',host], (error,stdout, stderr) => {
        if (error) {
            return res.send(`Error: ${stderr}`);
        }
        res.send(`<pre>${stdout}</pre>`);
    });

});

app.listen(3000, () => {
    console.log('ping app running on http://localhost:3000');
});
