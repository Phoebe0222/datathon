// const PythonShell = require('python-shell');

// var command = 'open1';
// var comport = 6;

// var options = {
//     scriptPath: 'python/scripts',
//     args: [command, comport]
// };

// PythonShell.PythonShell.run('hello.py', options, function (err, results) {
//   console.log('results: %j', results);
// });

////

// import express JS module into app 
// and creates its variable. 
var express = require('express'); 
var app = express(); 
var multer = require('multer')
var cors = require('cors');
var name = 'yo'; 
// Creates a server which runs on port 3000 and  
// can be accessed through localhost:3000 
// Access-Control-Allow-Origin: *

// var corsOptions = {
//   // origin: 'http://example.com',
//   // optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
//   Access-Control-Allow-Origin: *
// }


app.listen(3000, function() { 
    console.log('server running on port 3000'); 
} ) 
app.post('/upload',function(req, res) {
     
    upload(req, res, function (err) {

      return "res.status(200).send(req.file)"

    })

});
// Function callName() is executed whenever  
// url is of the form localhost:3000/name 
app.get('/upload', callName); 
  
function callName(req, res) { 
      
    // Use child_process.spawn method from  
    // child_process module and assign it 
    // to variable spawn 
    res.header("Access-Control-Allow-Origin", "*");
    var spawn = require("child_process").spawn; 
      
    // Parameters passed in spawn - 
    // 1. type_of_script 
    // 2. list containing Path of the script 
    //    and arguments for the script  
      
    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will 
    // so, first name = Mike and last name = Will 
    var process = spawn('python',["./hello.py", 
                            name, 
                            req.query.lastname] ); 
  
    // Takes stdout data from script which executed 
    // with arguments and send this data to res object 
    process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
    } ) 
} 
  