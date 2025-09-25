from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas


app = FastAPI(title="E-Commerce API")

# Dependency: DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Items ----------
@app.get("/items", response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ---------- Orders ----------

@app.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, updated: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.item_id = updated.item_id
    db_order.quantity = updated.quantity
    db_order.status = updated.status

    db.commit()
    db.refresh(db_order)
    return db_order

# DELETE order by ID
@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"detail": f"Order {order_id} deleted successfully"}

# GET all sales transactions 
@app.get("/sales", response_model=list[schemas.Order])
def get_sales(db: Session = Depends(get_db)):
    """
    Get all sales transactions (currently same as orders).
    """
    return db.query(models.Order).all()
# Create DB tables
models.Base.metadata.create_all(bind=database.engine)
