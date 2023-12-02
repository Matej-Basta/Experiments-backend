const express = require('express');
const path = require('path');
const app = express();
const fs = require('fs');

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => console.log("Server started on port " + PORT));

app.get('/', (req, res) => {
    const numberOfElements = req.query.numberOfElements || 5;
    
    const indexPath = path.join(__dirname, 'build', 'index.html');
    fs.readFile(indexPath, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send('An error occurred');
        }
        const modifiedHTML = data.replace('{{numberOfElements}}', numberOfElements);
        
        res.send(modifiedHTML);
    });
}); 
app.use(express.static(path.join(__dirname, 'build')));
