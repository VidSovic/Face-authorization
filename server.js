const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) =>{
        const spawn = require("child_process").spawn;
        const arg1 = "./mojObraz2.jpg"
        const arg2 = "./obrazNejc.jpg"
        const pythonProcess = spawn('python', ["./test.py", arg1, arg2]);

        pythonProcess.stdout.on('data', (data)=>{
            console.log(data.toString())
            res.write(data);
            res.end('end');
        });
})

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))