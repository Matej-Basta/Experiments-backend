const express = require('express');
const path = require('path');
const app = express();
const fs = require('fs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const App = require('./src/App').default;

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => console.log("Server started on port " + PORT));
app.use('/assets', express.static(path.join(__dirname, 'src', 'assets')));

app.get('/', (req, res, next) => {
    const numberOfElements = req.query.numberOfElements || 5;
    
    const indexPath = path.join(__dirname, 'build', 'index.html');
    fs.readFile(indexPath, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send('An error occurred');
        }
        const modifiedHTML = data.replace('{{numberOfElements}}', numberOfElements);
        
        return res.send(modifiedHTML.replace('<div id="root"></div>', `<div id="root">${ReactDOMServer.renderToString(<App numberOfElements={numberOfElements}/>)}</div>`));
    });
}); 

app.use(express.static(path.join(__dirname, 'build')));