#!/usr/bin/env python

from backend import manager
from backend import app

if __name__ == '__main__':
    manager.run()
    #app.run()
    #app.run(host='0.0.0.0', port=5000, debug=False)
