from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductResponse
from auth import verify_token
from typing import List

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# CREATE - Add a new product
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# READ ALL - Get all products
@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    products = db.query(Product).all()
    return products

# READ ONE - Get a single product by ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

# UPDATE - Edit a product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

# DELETE - Remove a product
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted successfully"}