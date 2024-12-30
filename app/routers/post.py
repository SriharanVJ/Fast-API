from .. import schemas,models,oauth2
from fastapi import Depends,status,HTTPException,APIRouter,Response
from sqlalchemy.orm import Session
from random import randrange
from .. database import get_db
from typing import List,Optional

router=APIRouter()



my_posts=[{"title":"favourite food","content":"i like pizza","id":1},
          {"title":"favourite book","content":"i like book","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i
    


@router.post("/posts")
def createpost(new_post:schemas.PostCreate):
    post_dict=new_post.dict()
    post_dict["id"]=randrange(0,100)
    my_posts.append(post_dict)
    
    
    return my_posts

@router.get("/posts/{id}")
def get_post(id):
    post=find_post(int(id))
    return {"message":post}

@router.get("/posts/recent/latest")
def latest_post():
    latest=my_posts[len(my_posts)-1]
    return {"latest post":latest}

@router.put("/posts/{id}")
def update_post(id:int,post:schemas.PostCreate):
    index=find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    post_dict=post.dict()
    post_dict["id"]=id
    my_posts[index]=post_dict
    
    
    return {"message":post_dict}

@router.delete("/posts/{id}")
def delete_post(id):
    index=find_index_post(int(id))
    
    my_posts.pop(index)
    return {"message":"post deleted"}




@router.get("/sqlalchemy",response_model=List[schemas.Post])
def test_posts(db:Session=Depends(get_db),user_id=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).all()
    return post

@router.get("/sqlalchamy",response_model=schemas.Post)
def test_posts(db:Session=Depends(get_db),
limit:int=10,skip:int=0,search:Optional[str]=""):
    print(limit)
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return {"return":post}
    
@router.post("/sql",response_model=schemas.Post)
def get_sql(post:schemas.PostCreate,db:Session=Depends(get_db)):
    posts=models.Post(**post.dict()    )
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

@router.get("/sqlposts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return {"Here your status":post}

@router.delete("/sqlposts/{id}",response_model=schemas.Post)
def delete_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return {"message":"post deleted"}
    
    
@router.put("/sqlposts/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id==id)

    post=post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    
    post_query.update({"title":"its very interesting","content":"take opposite"})
    db.commit()

    return {"message":"post updated"}


@router.post("/createbook",response_model=schemas.Book)
def new_book(new:schemas.Book,db:Session=Depends(get_db)):
    new=models.Books(**new.dict())
    db.add(new)
    db.commit(new)
    db.refresh(new)
    
    return new    