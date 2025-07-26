from app import db
from datetime import datetime
from sqlalchemy import Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Utilizador(db.Model):
    __tablename__ = 'utilizadores'
    
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(Text, nullable=False)
    nome_completo = db.Column(Text)
    funcao = db.Column(Text)
    telemovel = db.Column(Text)
    
    # Relationship with locations
    localizacoes = relationship("Localizacao", back_populates="utilizador", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Utilizador {self.username}>'

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'
    
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('utilizadores.id'), nullable=False)
    latitude = db.Column(Numeric(10, 6), nullable=False)
    longitude = db.Column(Numeric(10, 6), nullable=False)
    precisao = db.Column(Numeric(5, 2))
    timestamp = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship with user
    utilizador = relationship("Utilizador", back_populates="localizacoes")
    
    def __repr__(self):
        return f'<Localizacao {self.latitude}, {self.longitude}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.utilizador.username if self.utilizador else None,
            'nome_completo': self.utilizador.nome_completo if self.utilizador else None,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'precisao': float(self.precisao) if self.precisao else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
