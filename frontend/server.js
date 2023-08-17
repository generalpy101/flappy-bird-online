const express = require('express')
const morgan = require('morgan')
const axios = require('axios')
const dotenv = require('dotenv')

const path = require('path')

dotenv.config()

const HOST = process.env.HOST || 'localhost'
const PORT = process.env.PORT || 3000

const BASE_PATH = path.join(__dirname)
const PUBLIC_PATH = path.join(BASE_PATH, 'public')
const STATIC_PATH = path.join(BASE_PATH, 'public', 'static')

const ENV = process.env.NODE_ENV || 'development'

const app = express()

if (ENV === 'development') {
  app.use(morgan('dev'))
} else {
    app.use(morgan('combined'))
}

// Add static files path
app.use('/static', express.static(STATIC_PATH))
// Add json parser
app.use(express.json())

app.get('/', (req, res) => {
    res.sendFile(path.join(PUBLIC_PATH, 'index.html'))
})

app.listen(PORT, HOST, () => {
    console.log(`Server running on ${HOST}:${PORT}`)
})