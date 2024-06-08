from fastapi import FastAPI
import uvicorn
from routes.gets.get_routes import router as router_get
from routes.posts.post_routes import router as router_post
from api.api import router as router_api
import ssl
from pathlib import Path
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from fastapi.middleware.cors import CORSMiddleware



origins = [
    'https://127.0.0.1:8000',
    'http://127.0.0.1:8000',
    "https://13.60.35.192.traefik.me",
    'https://journal-interactive-1.onrender.com'
]





app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods = ['*'],allow_headers=['*'])

app.include_router(router_get)
app.include_router(router_post)
app.include_router(router_api)






if __name__ == '__main__':
    
    uvicorn.run('app:app',reload=True,port=30000)
