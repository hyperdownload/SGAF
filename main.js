const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const http = require('http');

let flaskProcess;
let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        autoHideMenuBar: true,
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    //Carga la URL del servidor Flask
    mainWindow.loadURL('http://127.0.0.1:5000');

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function startFlask() {
    flaskProcess = spawn('python', ['pruebaflask.py'], { shell: true });

    //Verifica cada segundo si el servidor Flask está listo
    const checkServer = setInterval(() => {
        http.get('http://127.0.0.1:5000', (res) => {
            if (res.statusCode === 200) {
                clearInterval(checkServer); 
                createWindow(); //Abre la ventana de Electron
            }
        }).on('error', () => {
            //Si hay error, flask todavia no esta listo
        });
    }, 1000); //Verifica cada segundo
}

app.whenReady().then(() => {
    startFlask(); //Inicia Flask y verifica cuando este listo

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (flaskProcess) flaskProcess.kill(); // Frena en seco a flask
    if (process.platform !== 'darwin') app.quit();
});
