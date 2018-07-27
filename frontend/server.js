#!/usr/bin/env node
const
  express = require('express'),
  serveStatic = require('serve-static'),
  history = require('connect-history-api-fallback'),
  port = process.env.PORT || 8000

const app = express()

app.use(history())
app.use(serveStatic('./dist/spa-mat'))
app.listen(port)
