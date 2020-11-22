import uvicorn

from abilling.app.fastapi import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', port=5000, reload=True)
