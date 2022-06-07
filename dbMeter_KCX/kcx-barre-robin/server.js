const express = require('express')
const {createServer} = require("http");
const fs = require('fs')
const {Server} = require('socket.io')

const app = express()
const httpServer = createServer(app)

app.use(express.static('public', {extensions: ['html']}));

app.get('*', (req, res) => {
  res.redirect('/barre')
})

const io = new Server(httpServer)

let showRecords = false
let scoreKC = 0
let scoreKOI = 0

setInterval(() => {
  fs.readFile('./test.json', 'utf8', (err, data) => {
    if (err) {
      console.error(err)
      return
    }
    
    io.emit('current', data)
  })
}, 100)

io.on('connection', client => {
  console.log('Client connected')

  client.emit('recordsState', showRecords)
  client.emit('kc', scoreKC)
  client.emit('koi', scoreKOI)

  client.on('toggleRecords', show => {
    showRecords = show
    io.emit('toggleRecords', show)
  })

  client.on('kc', score => {
    scoreKC = score
    io.emit('kc', score)
  })

  client.on('koi', score => {
    scoreKOI = score
    io.emit('koi', score)
  })

  client.on('disconnect', () => {
    console.log('Client disconnected')
  })
})

httpServer.listen(2022, () => {
  console.log('Server running on port 2022')
})
