from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user,auth,vote
from . config import settings



models.Base.metadata.create_all(bind=engine)


    

my_posts=[{"title":"favourite food","content":"i like pizza","id":1},
          {"title":"favourite book","content":"i like book","id":2}]




    
app=FastAPI()




@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"my_posts":my_posts}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)