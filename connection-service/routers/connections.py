from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.connection import Connection
from schemas.connection import ConnectionCreate, ConnectionUpdate, ConnectionResponse
from auth.jwt import verify_token
from typing import List

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/", response_model=ConnectionResponse, status_code=201)
def send_connection(
    data: ConnectionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    if data.receiver_id == user_id:
        raise HTTPException(status_code=400, detail="Tidak bisa connect ke diri sendiri")
    existing = db.query(Connection).filter(
        Connection.sender_id == user_id,
        Connection.receiver_id == data.receiver_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permintaan sudah dikirim")
    conn = Connection(sender_id=user_id, receiver_id=data.receiver_id)
    db.add(conn)
    db.commit()
    db.refresh(conn)
    return conn

@router.get("/", response_model=List[ConnectionResponse])
def get_all_connections(db: Session = Depends(get_db)):
    return db.query(Connection).all()

@router.get("/me", response_model=List[ConnectionResponse])
def my_connections(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return db.query(Connection).filter(
        (Connection.sender_id == user_id) | (Connection.receiver_id == user_id)
    ).all()

@router.get("/{connection_id}", response_model=ConnectionResponse)
def get_connection(connection_id: int, db: Session = Depends(get_db)):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Koneksi tidak ditemukan")
    return conn

@router.put("/{connection_id}", response_model=ConnectionResponse)
def update_status(
    connection_id: int,
    data: ConnectionUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Koneksi tidak ditemukan")
    if conn.receiver_id != user_id:
        raise HTTPException(status_code=403, detail="Hanya penerima yang bisa update status")
    conn.status = data.status
    db.commit()
    db.refresh(conn)
    return conn

@router.delete("/{connection_id}", status_code=204)
def delete_connection(
    connection_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Koneksi tidak ditemukan")
    if conn.sender_id != user_id:
        raise HTTPException(status_code=403, detail="Hanya pengirim yang bisa hapus")
    db.delete(conn)
    db.commit()