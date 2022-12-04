#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uvicorn

if __name__ == "__main__":
    uvicorn.run('app.main:app', host="0.0.0.0", port=8042, reload=True,
                headers=[('Server', 'custom'), ('Connection', 'close')],
                proxy_headers=True)
