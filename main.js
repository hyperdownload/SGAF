const { app, BrowserWindow, dialog } = require('electron');
const { spawn, exec } = require('child_process');
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

    // Carga la URL del servidor Flask
    mainWindow.loadURL('http://127.0.0.1:5000');

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function isPythonInstalled(callback) {
    exec('python --version', (error, stdout, stderr) => {
        if (error) {
            callback(false);
        } else {
            callback(true);
        }
    });
}

function installPython() {
    dialog.showMessageBox({
        type: 'info',
        buttons: ['Abrir página de Python', 'Cancelar'],
        defaultId: 0,
        message: 'Python no está instalado. Necesitas instalarlo para continuar.',
        detail: 'Haz clic en "Abrir página de Python" para descargarlo e instalarlo.'
    }).then(response => {
        if (response.response === 0) {
            // Abre la pagina de descarga de Python
            require('electron').shell.openExternal('https://www.python.org/downloads/');
        }
    });
}

function startFlask() {
    flaskProcess = spawn('python', ['pruebaflask.py'], { shell: true });

    flaskProcess.stdout.on('data', (data) => {
        console.log(`Flask: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`Flask error: ${data}`);
    });

    flaskProcess.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });

    // Verifica cada segundo si el servidor Flask esta listo
    const checkServer = setInterval(() => {
        http.get('http://127.0.0.1:5000', (res) => {
            if (res.statusCode === 200) {
                clearInterval(checkServer); 
                createWindow(); // Abre la ventana de Electron
            }
        }).on('error', () => {
            // Si hay error, Flask todavia no esta listo
        });
    }, 1000); // Verifica cada segundo
}

function stopFlask() {
    if (flaskProcess) {
        console.log('Cerrando Flask...');
        flaskProcess.kill('SIGINT'); // Envia la señal para finalizar el proceso
        flaskProcess = null;
    }
}

app.whenReady().then(() => {
    isPythonInstalled(isInstalled => {
        if (isInstalled) {
            startFlask(); // Inicia Flask y verifica cuando este listo
        } else {
            installPython(); // Notifica al usuario que necesita instalar Python
        }
    });

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    stopFlask(); // Detiene Flask cuando todas las ventanas están cerradas
    if (process.platform !== 'darwin') app.quit();
});

app.on('quit', function () {
    stopFlask(); // Asegura que Flask se detenga si se llama a `app.quit()`
});
