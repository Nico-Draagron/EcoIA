import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageEnhance
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import os
import json
from datetime import datetime, timedelta
import time
from typing import Tuple, Dict, List, Optional
import base64
from io import BytesIO

# ================================================
# 🎨 CONFIGURAÇÕES INICIAIS
# ================================================

st.set_page_config(
    page_title="🌱 EcoDetector v2.0",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Nico-Draagron/EcoIA',
        'Report a bug': "https://github.com/Nico-Draagron/EcoIA/issues",
        'About': "EcoDetector v2.0 - Sistema Inteligente de Reciclagem"
    }
)

# ================================================
# 🎨 ESTILOS CSS AVANÇADOS
# ================================================

def load_css():
    st.markdown("""
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e base */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fundo principal com gradiente dinâmico */
    .main {
        background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 25%, #f0f9f0 50%, #e8f5e8 75%, #f8fffe 100%);
        background-size: 400% 400%;
        animation: gradientSht 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar moderna */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a1e 0%, #2d5a2d 50%, #3e8e41 100%);
        box-shadow: 4px 0 15px rgba(0,0,0,0.1);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Header principal com glass effect */
    .eco-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,255,248,0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .eco-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Cards com glass morphism */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,255,248,0.95));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    /* Cards de predição com efeito neon */
    .prediction-card {
        background: linear-gradient(135deg, #ffffff, #f8fff8);
        border: 2px solid #3e8e41;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(62, 142, 65, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(62, 142, 65, 0.3); }
        to { box-shadow: 0 0 30px rgba(62, 142, 65, 0.5); }
    }
    
    /* Cards de EcoMoedas com animação */
    .ecomoeda-card {
        background: linear-gradient(135deg, #fff3cd, #ffe69c, #ffd700);
        border: 3px solid #f39c12;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(243, 156, 18, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Métricas modernas */
    .modern-metric {
        background: linear-gradient(135deg, #ffffff, #f8fff8);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(62, 142, 65, 0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .modern-metric:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d5a2d;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Badges de medalhas */
    .medal-badge {
        display: inline-block;
        padding: 0.8rem 1.2rem;
        margin: 0.3rem;
        border-radius: 25px;
        font-weight: 600;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .medal-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .medal-bronze { background: linear-gradient(45deg, #cd7f32, #b8860b); }
    .medal-silver { background: linear-gradient(45deg, #c0c0c0, #a8a8a8); }
    .medal-gold { background: linear-gradient(45deg, #ffd700, #ffb300); }
    .medal-diamond { background: linear-gradient(45deg, #b9f2ff, #87ceeb); }
    
    /* Botões modernos */
    .stButton > button {
        background: linear-gradient(45deg, #3e8e41, #28a745);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #28a745, #1e7e34);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }
    
    /* Indicadores de confiança */
    .confidence-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .confidence-high { 
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .confidence-medium { 
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .confidence-low { 
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    /* Alertas personalizados */
    .custom-alert {
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-left-color: #28a745;
        color: #155724;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border-left-color: #ffc107;
        color: #856404;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    /* Seção de upload com drag & drop visual */
    .upload-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,255,248,0.9));
        border: 2px dashed #3e8e41;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #28a745;
        background: linear-gradient(135deg, rgba(248,255,248,0.95), rgba(240,249,240,0.95));
    }
    /* Cards de recompensa */
/* Cards de recompensa */
    .reward-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border: 2px solid #6c757d;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .reward-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-color: #28a745;
    }

    .reward-card.disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .reward-card.disabled:hover {
        transform: none;
        box-shadow: none;
    }
    /* Animações de loading */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3e8e41;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .eco-header {
            padding: 1rem;
        }
        
        .glass-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
    
    /* Ocultar elementos do Streamlit */
    .css-1jc7ptx, .css-1aumxhk, .css-1d391kg .css-1aumxhk {
        background: transparent;
    }
    
    .css-k1vhr4 {
        margin-top: -75px;
    }
    
    /* Customização do sidebar */
    .css-1d391kg .css-1v0mbdj {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ================================================
# 🗂️ DADOS E CONFIGURAÇÕES
# ================================================

# Classes do modelo
CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Configurações do modelo
MODEL_CONFIG = {
    'input_size': (224, 224),
    'model_path': 'modelo_oikos.pt',
    'confidence_threshold': 0.65,
    'min_confidence_threshold': 0.35,
    'entropy_threshold': 1.8,
    'max_probability_threshold': 0.45
}

# Metadados das classes
CLASS_METADATA = {
    'cardboard': {
        'emoji': '📦', 'name': 'Papelão', 'recyclable': True, 'color': '#8B4513',
        'tips': [
            "Desmonte as caixas para economizar espaço",
            "Remova fitas adesivas e grampos metálicos",
            "Mantenha seco - papelão molhado não é reciclável",
            "💡 Pode ser transformado em novos produtos!"
        ],
        'curiosidade': "O papelão pode ser reciclado até 7 vezes consecutivas!"
    },
    'glass': {
        'emoji': '🍾', 'name': 'Vidro', 'recyclable': True, 'color': '#4CAF50',
        'tips': [
            "Remova tampas e rótulos quando possível",
            "Não misture com vidros temperados ou espelhos",
            "Vidros quebrados devem ser embrulhados",
            "💡 O vidro é 100% reciclável infinitas vezes!"
        ],
        'curiosidade': "1 tonelada de vidro reciclado economiza 1.2 toneladas de matéria-prima!"
    },
    'metal': {
        'emoji': '🥫', 'name': 'Metal', 'recyclable': True, 'color': '#FF9800',
        'tips': [
            "Lave para remover restos de comida",
            "Amasse latas para economizar espaço",
            "Separe alumínio de outros metais",
            "💡 Economiza até 95% de energia!"
        ],
        'curiosidade': "Uma lata de alumínio vira nova lata em apenas 60 dias!"
    },
    'paper': {
        'emoji': '📄', 'name': 'Papel', 'recyclable': True, 'color': '#2196F3',
        'tips': [
            "Evite papéis com cera ou plastificação",
            "Remova grampos e clipes metálicos",
            "Papéis sujos de óleo não são recicláveis",
            "💡 Salva árvores e reduz poluição!"
        ],
        'curiosidade': "1 tonelada de papel reciclado economiza 3.3m³ de madeira!"
    },
    'plastic': {
        'emoji': '🧴', 'name': 'Plástico', 'recyclable': True, 'color': '#E91E63',
        'tips': [
            "Verifique o código de reciclagem (1-7)",
            "Lave para remover resíduos",
            "Remova tampas se forem de material diferente",
            "💡 Pode virar roupas e carpetes!"
        ],
        'curiosidade': "5 garrafas PET podem virar uma camiseta!"
    },
    'trash': {
        'emoji': '🚮', 'name': 'Lixo Comum', 'recyclable': False, 'color': '#757575',
        'tips': [
            "Não é reciclável pelos métodos convencionais",
            "Descarte no lixo comum adequado",
            "Considere reduzir o uso deste tipo",
            "💡 Repense, reduza, reutilize!"
        ],
        'curiosidade': "A melhor opção é sempre reduzir o consumo!"
    }
}

# Sistema de EcoMoedas
ECOMOEDA_SISTEMA = {
    'cardboard': {'valor': 15, 'impacto': {'co2': 1.2, 'energia': 0.8, 'agua': 2.5}, 'raridade': 'comum'},
    'paper': {'valor': 12, 'impacto': {'co2': 0.9, 'energia': 0.6, 'agua': 3.2}, 'raridade': 'comum'},
    'plastic': {'valor': 25, 'impacto': {'co2': 2.1, 'energia': 1.8, 'agua': 1.5}, 'raridade': 'raro'},
    'glass': {'valor': 20, 'impacto': {'co2': 1.8, 'energia': 2.2, 'agua': 0.8}, 'raridade': 'raro'},
    'metal': {'valor': 35, 'impacto': {'co2': 3.5, 'energia': 4.2, 'agua': 2.8}, 'raridade': 'épico'},
    'trash': {'valor': 0, 'impacto': {'co2': 0, 'energia': 0, 'agua': 0}, 'raridade': 'comum'}
}

# Sistema de medalhas
MEDALHAS = {
    'primeiro_scan': {'nome': 'Primeira Detecção', 'emoji': '🎯', 'desc': 'Primeira análise realizada'},
    'eco_iniciante': {'nome': 'Eco Iniciante', 'emoji': '🌱', 'desc': '50+ EcoMoedas'},
    'eco_guerreiro': {'nome': 'Eco Guerreiro', 'emoji': '🛡️', 'desc': '200+ EcoMoedas'},
    'eco_heroi': {'nome': 'Eco Herói', 'emoji': '🦸', 'desc': '500+ EcoMoedas'},
    'especialista_plastico': {'nome': 'Especialista Plástico', 'emoji': '🧴', 'desc': '10 plásticos'},
    'mestre_metal': {'nome': 'Mestre Metal', 'emoji': '🥫', 'desc': '10 metais'},
    'guardian_vidro': {'nome': 'Guardião Vidro', 'emoji': '🍾', 'desc': '10 vidros'},
    'streak_7': {'nome': 'Sequência 7', 'emoji': '🔥', 'desc': '7 corretas seguidas'}
}
# Sistema de recompensas
RECOMPENSAS = {
    'roupas': {
        'camiseta_eco': {
            'nome': 'Camiseta EcoWarrior',
            'emoji': '👕',
            'custo': 150,
            'desc': 'Camiseta sustentável feita com algodão orgânico',
            'categoria': 'Roupas'
        },
        'mochila_reciclada': {
            'nome': 'Mochila Eco',
            'emoji': '🎒',
            'custo': 300,
            'desc': 'Mochila feita com materiais reciclados',
            'categoria': 'Roupas'
        },
        'bone_eco': {
            'nome': 'Boné Verde',
            'emoji': '🧢',
            'custo': 100,
            'desc': 'Boné com tecido sustentável',
            'categoria': 'Roupas'
        }
    },
    'cesta_basica': {
        'cesta_pequena': {
            'nome': 'Cesta Básica P',
            'emoji': '🥫',
            'custo': 200,
            'desc': 'Cesta com 10 itens essenciais',
            'categoria': 'Alimentação'
        },
        'cesta_media': {
            'nome': 'Cesta Básica M',
            'emoji': '🛒',
            'custo': 350,
            'desc': 'Cesta com 20 itens variados',
            'categoria': 'Alimentação'
        },
        'cesta_grande': {
            'nome': 'Cesta Básica G',
            'emoji': '📦',
            'custo': 500,
            'desc': 'Cesta completa para família',
            'categoria': 'Alimentação'
        }
    },
    'material_escolar': {
        'kit_basico': {
            'nome': 'Kit Escolar Básico',
            'emoji': '✏️',
            'custo': 80,
            'desc': 'Lápis, canetas e borracha ecológicos',
            'categoria': 'Escolar'
        },
        'caderno_reciclado': {
            'nome': 'Caderno Reciclado',
            'emoji': '📓',
            'custo': 50,
            'desc': 'Caderno 200 folhas de papel reciclado',
            'categoria': 'Escolar'
        },
        'kit_completo': {
            'nome': 'Kit Escolar Completo',
            'emoji': '🎓',
            'custo': 250,
            'desc': 'Material completo para o ano letivo',
            'categoria': 'Escolar'
        }
    }
}
# Pontos de coleta (dados simplificados do RS)
PONTOS_COLETA = {
    'cardboard': [
        {'cidade': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'nome': 'Ecoponto Centro', 'endereco': 'Av. Borges de Medeiros, 1501', 'horario': '8h-17h', 'telefone': '(51) 3289-6000'},
        {'cidade': 'Porto Alegre', 'lat': -30.0568, 'lon': -51.1733, 'nome': 'Cooperativa COOPERTINGA', 'endereco': 'Rua Santana, 1200', 'horario': '7h-16h', 'telefone': '(51) 3225-1234'},
        {'cidade': 'Caxias do Sul', 'lat': -29.1634, 'lon': -51.1797, 'nome': 'Central de Reciclagem Caxias', 'endereco': 'Rua Ludovico Cavinato, 1555', 'horario': '8h-17h', 'telefone': '(54) 3290-5500'},
        {'cidade': 'Pelotas', 'lat': -31.7654, 'lon': -52.3376, 'nome': 'Ecoponto Pelotas Sul', 'endereco': 'Av. Bento Gonçalves, 3344', 'horario': '8h-16h', 'telefone': '(53) 3227-8800'},
        {'cidade': 'Santa Maria', 'lat': -29.6842, 'lon': -53.8069, 'nome': 'COOMARSUL', 'endereco': 'Rua Appel, 1456', 'horario': '7h30-17h', 'telefone': '(55) 3212-9900'},
        {'cidade': 'Canoas', 'lat': -29.9177, 'lon': -51.1794, 'nome': 'Ecoponto Canoas', 'endereco': 'Av. Guilherme Schell, 5340', 'horario': '8h-17h', 'telefone': '(51) 3464-7700'},
        {'cidade': 'Novo Hamburgo', 'lat': -29.6783, 'lon': -51.1309, 'nome': 'Cooperativa COOPERTEC', 'endereco': 'Rua Gen. Daltro Filho, 1200', 'horario': '8h-16h', 'telefone': '(51) 3525-2200'},
        {'cidade': 'Passo Fundo', 'lat': -28.2636, 'lon': -52.4091, 'nome': 'COOTRAVIPA', 'endereco': 'Rua Uruguai, 2567', 'horario': '7h-17h', 'telefone': '(54) 3311-4400'}
    ],
    'plastic': [
        {'cidade': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'nome': 'Ecoponto Centro', 'endereco': 'Av. Borges de Medeiros, 1501', 'horario': '8h-17h', 'telefone': '(51) 3289-6000'},
        {'cidade': 'Porto Alegre', 'lat': -30.1059, 'lon': -51.2019, 'nome': 'PET Recicla POA', 'endereco': 'Rua Cristóvão Colombo, 545', 'horario': '8h-17h', 'telefone': '(51) 3330-1100'},
        {'cidade': 'Caxias do Sul', 'lat': -29.1877, 'lon': -51.1589, 'nome': 'PlásticoVerde Caxias', 'endereco': 'Av. Júlio de Castilhos, 2890', 'horario': '8h-16h', 'telefone': '(54) 3223-3300'},
        # Adicione mais pontos conforme necessário
    ],
    'glass': [
        {'cidade': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'nome': 'Ecoponto Centro', 'endereco': 'Av. Borges de Medeiros, 1501', 'horario': '8h-17h', 'telefone': '(51) 3289-6000'},
        {'cidade': 'Porto Alegre', 'lat': -30.0275, 'lon': -51.2287, 'nome': 'VidroLimpo POA', 'endereco': 'Rua Riachuelo, 1333', 'horario': '8h-17h', 'telefone': '(51) 3286-7700'},
        # Adicione mais pontos conforme necessário
    ],
    'metal': [
        {'cidade': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'nome': 'Ecoponto Centro', 'endereco': 'Av. Borges de Medeiros, 1501', 'horario': '8h-17h', 'telefone': '(51) 3289-6000'},
        {'cidade': 'Porto Alegre', 'lat': -30.0194, 'lon': -51.2189, 'nome': 'MetalRecicla POA', 'endereco': 'Av. Ipiranga, 6681', 'horario': '7h-17h', 'telefone': '(51) 3320-5500'},
        {'cidade': 'Caxias do Sul', 'lat': -29.1456, 'lon': -51.1945, 'nome': 'FerroVelho Caxias', 'endereco': 'Rua Sinimbu, 1890', 'horario': '7h30-17h30', 'telefone': '(54) 3221-8800'},
        # Adicione mais pontos conforme necessário
    ],
    'paper': [
        {'cidade': 'Porto Alegre', 'lat': -30.0346, 'lon': -51.2177, 'nome': 'Ecoponto Centro', 'endereco': 'Av. Borges de Medeiros, 1501', 'horario': '8h-17h', 'telefone': '(51) 3289-6000'},
        {'cidade': 'Caxias do Sul', 'lat': -29.1634, 'lon': -51.1797, 'nome': 'Central de Reciclagem Caxias', 'endereco': 'Rua Ludovico Cavinato, 1555', 'horario': '8h-17h', 'telefone': '(54) 3290-5500'},
        # Adicione mais pontos conforme necessário
    ]
}

# ================================================
# 🔧 FUNÇÕES AUXILIARES
# ================================================

def inicializar_sessao():
    """Inicializa dados da sessão"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'ecomoedas_total': 0,
            'deteccoes_realizadas': 0,
            'historico_deteccoes': [],
            'medalhas_conquistadas': [],
            'impacto_total': {'co2': 0.0, 'energia': 0.0, 'agua': 0.0},
            'contadores_classe': {classe: 0 for classe in CLASSES},
            'streak_atual': 0,
            'nivel_usuario': 1,
            'xp_total': 0,
            'data_ultimo_acesso': datetime.now().isoformat(),
            'recompensas_resgatadas': []
        }
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Detector'

def salvar_deteccao(classe: str, confianca: float, ecomoedas: int):
    """Salva detecção e atualiza estatísticas"""
    deteccao = {
        'timestamp': datetime.now().isoformat(),
        'classe': classe,
        'confianca': confianca,
        'ecomoedas': ecomoedas,
        'impacto': ECOMOEDA_SISTEMA[classe]['impacto']
    }
    
    user_data = st.session_state.user_data
    user_data['historico_deteccoes'].append(deteccao)
    user_data['ecomoedas_total'] += ecomoedas
    user_data['deteccoes_realizadas'] += 1
    user_data['contadores_classe'][classe] += 1
    user_data['xp_total'] += ecomoedas * 2
    
    # Atualizar impacto
    impacto = ECOMOEDA_SISTEMA[classe]['impacto']
    user_data['impacto_total']['co2'] += impacto['co2']
    user_data['impacto_total']['energia'] += impacto['energia']
    user_data['impacto_total']['agua'] += impacto['agua']
    
    # Atualizar nível
    novo_nivel = min(10, user_data['xp_total'] // 100 + 1)
    if novo_nivel > user_data['nivel_usuario']:
        user_data['nivel_usuario'] = novo_nivel
        return True, verificar_medalhas()
    
    return False, verificar_medalhas()

def verificar_medalhas():
    """Verifica e retorna novas medalhas"""
    user_data = st.session_state.user_data
    medalhas_atuais = set(user_data['medalhas_conquistadas'])
    novas_medalhas = []
    
    # Verificar cada tipo de medalha
    condicoes = {
        'primeiro_scan': user_data['deteccoes_realizadas'] >= 1,
        'eco_iniciante': user_data['ecomoedas_total'] >= 50,
        'eco_guerreiro': user_data['ecomoedas_total'] >= 200,
        'eco_heroi': user_data['ecomoedas_total'] >= 500,
        'especialista_plastico': user_data['contadores_classe']['plastic'] >= 10,
        'mestre_metal': user_data['contadores_classe']['metal'] >= 10,
        'guardian_vidro': user_data['contadores_classe']['glass'] >= 10,
    }
    
    for medalha_id, condicao in condicoes.items():
        if condicao and medalha_id not in medalhas_atuais:
            novas_medalhas.append(medalha_id)
    
    if novas_medalhas:
        user_data['medalhas_conquistadas'].extend(novas_medalhas)
    
    return novas_medalhas
def resgatar_recompensa(recompensa_id: str, categoria: str):
    """Resgata uma recompensa usando EcoMoedas"""
    user_data = st.session_state.user_data
    recompensa = RECOMPENSAS[categoria][recompensa_id]
    
    if user_data['ecomoedas_total'] >= recompensa['custo']:
        user_data['ecomoedas_total'] -= recompensa['custo']
        user_data['recompensas_resgatadas'].append({
            'id': recompensa_id,
            'nome': recompensa['nome'],
            'categoria': categoria,
            'timestamp': datetime.now().isoformat(),
            'custo': recompensa['custo']
        })
        return True
    return False

# ================================================
# 🤖 FUNÇÕES DO MODELO
# ================================================

@st.cache_resource(show_spinner="🤖 Carregando modelo de IA...")
def carregar_modelo():
    """Carrega o modelo treinado"""
    try:
        if not os.path.exists(MODEL_CONFIG['model_path']):
            st.error(f"❌ Modelo não encontrado: {MODEL_CONFIG['model_path']}")
            st.info("💡 Coloque o arquivo 'modelo_oikos.pt' na pasta do projeto")
            return None
        
        # Criar modelo EfficientNet-B0
        modelo = models.efficientnet_b0(weights=None)
        modelo.classifier[1] = nn.Linear(modelo.classifier[1].in_features, len(CLASSES))
        
        # Carregar pesos
        device = torch.device('cpu')
        modelo.load_state_dict(torch.load(MODEL_CONFIG['model_path'], map_location=device))
        modelo.eval()
        
        return modelo
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar modelo: {str(e)}")
        return None

# Transformações de imagem
transformacao = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def fazer_predicao(modelo, imagem):
    """Realiza predição na imagem"""
    if modelo is None:
        return None, 0, np.zeros(len(CLASSES)), True
    
    try:
        # Preprocessar imagem
        img_tensor = transformacao(imagem).unsqueeze(0)
        
        # Fazer predição
        with torch.no_grad():
            saida = modelo(img_tensor)
            prob = torch.nn.functional.softmax(saida[0], dim=0)
            
            classe_idx = torch.argmax(prob).item()
            classe_predita = CLASSES[classe_idx]
            confianca = prob[classe_idx].item()
            
            # Detectar outliers
            entropia = -torch.sum(prob * torch.log(prob + 1e-12)).item()
            max_prob = torch.max(prob).item()
            
            is_outlier = (
                confianca < MODEL_CONFIG['min_confidence_threshold'] or
                entropia > MODEL_CONFIG['entropy_threshold'] or
                max_prob < MODEL_CONFIG['max_probability_threshold']
            )
            
            return classe_predita, confianca, prob.numpy(), is_outlier
            
    except Exception as e:
        st.error(f"❌ Erro na predição: {str(e)}")
        return None, 0, np.zeros(len(CLASSES)), True

# ================================================
# 🎨 COMPONENTES VISUAIS
# ================================================

def criar_header():
    """Exibe apenas a imagem de fundo como banner"""

    image_path = "exemplos/tela_inicial.png"

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <style>
    .eco-header {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        height: 300px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }}
    </style>

    <div class="eco-header"></div>
    """, unsafe_allow_html=True)

def mostrar_metricas_usuario():
    """Mostra métricas do usuário"""
    user_data = st.session_state.user_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="modern-metric">
            <div class="metric-value">🪙 {user_data['ecomoedas_total']}</div>
            <div class="metric-label">EcoMoedas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="modern-metric">
            <div class="metric-value">🎯 {user_data['deteccoes_realizadas']}</div>
            <div class="metric-label">Detecções</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="modern-metric">
            <div class="metric-value">🏆 {len(user_data['medalhas_conquistadas'])}</div>
            <div class="metric-label">Medalhas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="modern-metric">
            <div class="metric-value">⭐ {user_data['nivel_usuario']}</div>
            <div class="metric-label">Nível</div>
        </div>
        """, unsafe_allow_html=True)

def mostrar_grafico_probabilidades(probabilidades):
    """Cria gráfico de probabilidades moderno"""
    df = pd.DataFrame({
        'Classe': [CLASS_METADATA[cls]['name'] for cls in CLASSES],
        'Probabilidade': probabilidades * 100,
        'Cor': [CLASS_METADATA[cls]['color'] for cls in CLASSES]
    })
    
    fig = px.bar(
        df, 
        x='Probabilidade', 
        y='Classe',
        orientation='h',
        title='🎯 Análise de Probabilidades',
        color='Probabilidade',
        color_continuous_scale='Viridis',
        height=400
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        title_font_size=18,
        showlegend=False
    )
    
    return fig


def criar_mapa_interativo(material):
    """Cria mapa interativo melhorado com múltiplas camadas e visualizações"""
    
    pontos = PONTOS_COLETA.get(material, [])
    if not pontos:
        return None
    
    # Preparar dados para o mapa
    df_pontos = pd.DataFrame(pontos)
    
    # Adicionar cores e informações extras
    material_info = CLASS_METADATA.get(material, {})
    cor_rgb = hex_to_rgb(material_info.get('color', '#3e8e41'))
    cor_rgb.append(200)  # Alpha
    
    df_pontos['color'] = [cor_rgb] * len(df_pontos)
    df_pontos['radius'] = 300
    df_pontos['elevation'] = 50
    
    # Criar múltiplas camadas
    layers = []
    
    # 1. Camada de pontos principais (ScatterplotLayer)
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_pontos,
        get_position='[lon, lat]',
        get_color='color',
        get_radius='radius',
        radius_scale=1,
        radius_min_pixels=10,
        radius_max_pixels=60,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        line_width_min_pixels=3,
        get_line_color=[255, 255, 255, 255]
    )
    layers.append(scatter_layer)
    
    # 2. Camada de ícones (IconLayer)
    df_pontos['icon_data'] = [{
        'url': 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
        'width': 128,
        'height': 128,
        'anchorY': 128,
        'mask': True
    }] * len(df_pontos)
    
    icon_layer = pdk.Layer(
        'IconLayer',
        data=df_pontos,
        get_icon='icon_data',
        get_position='[lon, lat]',
        get_size=4,
        size_scale=15,
        pickable=True
    )
    layers.append(icon_layer)
    
    # 3. Camada de texto (TextLayer) para nomes das cidades
    df_cidades = df_pontos.groupby('cidade').first().reset_index()
    text_layer = pdk.Layer(
        'TextLayer',
        data=df_cidades,
        get_position='[lon, lat]',
        get_text='cidade',
        get_size=16,
        get_color=[0, 0, 0, 200],
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'bottom'",
        billboard=False,
        pickable=True
    )
    layers.append(text_layer)
    
    # 4. Camada de calor (HeatmapLayer) para densidade
    heatmap_layer = pdk.Layer(
        'HeatmapLayer',
        data=df_pontos,
        get_position='[lon, lat]',
        get_weight=1,
        radius_pixels=60,
        opacity=0.3,
        threshold=0.03
    )
    layers.append(heatmap_layer)
    
    # Configurar vista inicial centrada no RS
    view_state = pdk.ViewState(
        latitude=-30.0,
        longitude=-53.0,
        zoom=6.5,
        pitch=30,
        bearing=0
    )
    
    # Tooltip HTML melhorado
    tooltip_html = """
    <div style="font-family: 'Inter', sans-serif; background: rgba(255,255,255,0.98); 
         padding: 16px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); 
         max-width: 350px; border: 2px solid {cor};">
        
        <div style="display: flex; align-items: center; margin-bottom: 12px; 
                    border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">
            <span style="font-size: 2rem; margin-right: 10px;">{emoji}</span>
            <div>
                <h3 style="margin: 0; color: #2d5a2d; font-size: 1.2rem;">{nome}</h3>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">{cidade}, RS</p>
            </div>
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong style="color: #3e8e41;">📍 Endereço:</strong>
            <p style="margin: 2px 0 0 20px; color: #555;">{endereco}</p>
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong style="color: #3e8e41;">🕐 Horário:</strong>
            <span style="color: #555; margin-left: 5px;">{horario}</span>
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong style="color: #3e8e41;">📞 Telefone:</strong>
            <span style="color: #555; margin-left: 5px;">{telefone}</span>
        </div>
        
        <div style="background: linear-gradient(135deg, #e8f5e8, #d4f4d4); 
                    padding: 8px 12px; border-radius: 8px; margin-top: 12px; 
                    text-align: center;">
            <small style="color: #2d5a2d; font-weight: 600;">
                ♻️ Aceita: {material_nome}
            </small>
        </div>
        
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #ddd;">
            <small style="color: #888;">
                📅 Atualizado em: {data_atual}
            </small>
        </div>
    </div>
    """.format(
        cor=material_info.get('color', '#3e8e41'),
        emoji=material_info.get('emoji', '♻️'),
        nome='{nome}',
        cidade='{cidade}',
        endereco='{endereco}',
        horario='{horario}',
        telefone='{telefone}',
        material_nome=material_info.get('name', material),
        data_atual=datetime.now().strftime('%d/%m/%Y')
    )
    
    tooltip = {
        'html': tooltip_html,
        'style': {
            'backgroundColor': 'transparent',
            'color': 'black'
        }
    }
    
    # Criar deck com configurações melhoradas
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='mapbox://styles/mapbox/light-v10',
        map_provider='mapbox'
    )
    
    return deck

def criar_grafico_estatisticas(material):
    pontos = PONTOS_COLETA.get(material, [])
    if not pontos:
        return None

    df = pd.DataFrame(pontos)
    cidades = df['cidade'].value_counts().head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=cidades.index,
            y=cidades.values,
            marker_color=CLASS_METADATA.get(material, {}).get('color', '#3e8e41')
        )
    ])
    fig.update_layout(
        title="Top Cidades com Pontos de Coleta",
        xaxis_title="Cidade",
        yaxis_title="Quantidade de Pontos",
        template="simple_white"
    )
    return fig
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def criar_mapa_interativo(material, mostrar_calor=True, mostrar_nomes=True):
    """Cria visualização interativa com pontos, calor e nomes"""
    
    pontos = PONTOS_COLETA.get(material, [])
    if not pontos:
        return None

    df = pd.DataFrame(pontos)
    if df.empty or 'lat' not in df.columns or 'lon' not in df.columns:
        return None

    cor_rgb = hex_to_rgb(CLASS_METADATA.get(material, {}).get('color', '#3e8e41'))

    # Camada de pontos com cor personalizada
    layer_pontos = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_radius=5000,
        get_fill_color=list(cor_rgb) + [160],
        pickable=True,
        radius_min_pixels=5,
        radius_max_pixels=15,
    )

    layers = [layer_pontos]

    if mostrar_calor:
        layer_calor = pdk.Layer(
            "HeatmapLayer",
            data=df,
            get_position="[lon, lat]",
            aggregation=pdk.types.String("MEAN"),
            get_weight=1
        )
        layers.append(layer_calor)

    if mostrar_nomes:
        layer_texto = pdk.Layer(
            "TextLayer",
            data=df,
            get_position="[lon, lat]",
            get_text="cidade",
            get_size=16,
            get_color=[225, 225, 225],
            get_angle=0,
            get_alignment_baseline="'bottom'",
        )
        layers.append(layer_texto)

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=6,
        pitch=0,
    )

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "{nome} - {cidade}"}
    )
def mostrar_secao_mapa_melhorada(material):
    """Mostra seção do mapa com interface melhorada"""
    
    st.markdown("### 🗺️ Pontos de Coleta no Rio Grande do Sul")
    
    # Informações do material
    material_info = CLASS_METADATA.get(material, {})
    material_nome = material_info.get('name', material.title())
    material_emoji = material_info.get('emoji', '♻️')
    
    # Header com gradiente
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e8f5e8, #d4f4d4); 
                padding: 2rem; border-radius: 20px; margin-bottom: 2rem; 
                text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin: 0; color: #2d5a2d;">
            {material_emoji} Encontre onde descartar {material_nome}
        </h2>
        <p style="margin: 0.5rem 0 0 0; color: #3e8e41;">
            Localize os pontos de coleta mais próximos no Rio Grande do Sul
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar pontos disponíveis
    pontos = PONTOS_COLETA.get(material, [])
    
    if not pontos:
        st.warning(f"⚠️ Ainda não temos pontos de coleta para {material_nome} cadastrados.")
        return
    
    # Métricas em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #3e8e41;">📍 {len(pontos)}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Pontos Disponíveis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cidades_unicas = len(set(p['cidade'] for p in pontos))
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #3e8e41;">🏙️ {cidades_unicas}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Cidades Atendidas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #3e8e41;">🌍 RS</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Estado</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; color: #3e8e41;">{material_emoji}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">{material_nome}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Interativo", "📊 Estatísticas", "📋 Lista Detalhada"])
    
    with tab1:
        # Opções de visualização do mapa
        col_opt1, col_opt2 = st.columns([3, 1])
        
        with col_opt2:
            vista_3d = st.checkbox("🎮 Vista 3D", value=False)
            mostrar_calor = st.checkbox("🔥 Mapa de Calor", value=True)
            mostrar_nomes = st.checkbox("🏷️ Nomes das Cidades", value=True)
        
        # Criar e mostrar mapa
        try:
            # Chama a função criando o mapa com base nas opções selecionadas pelo usuário
            deck = criar_mapa_interativo(
                material=material,
                mostrar_calor=mostrar_calor,
                mostrar_nomes=mostrar_nomes
            )
            
            if deck:
                # Aplica rotação e inclinação se a vista 3D estiver ativada
                if vista_3d:
                    deck.initial_view_state.pitch = 45
                    deck.initial_view_state.bearing = -15

                # Exibe o mapa na interface Streamlit
                st.pydeck_chart(deck, use_container_width=True)

                # Instruções visuais para o usuário
                st.info("""
                💡 **Dicas de Navegação:**
                - 🖱️ **Clique e arraste** para mover o mapa  
                - 🔍 **Scroll** para zoom in/out  
                - 📍 **Clique nos pontos** para ver detalhes  
                - 🎮 **Segure Ctrl + arraste** para rotacionar (modo 3D)
                """)
            else:
                st.error("❌ Erro ao carregar o mapa")
        except Exception as e:
            st.error(f"❌ Erro ao criar o mapa: {str(e)}")
    
    with tab2:
        # Mostrar gráfico de estatísticas
        fig = criar_grafico_estatisticas(material)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas adicionais
        st.markdown("#### 📈 Análise de Cobertura")
        
        # Criar DataFrame para análise
        df_pontos = pd.DataFrame(pontos)
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            # Pontos por cidade
            pontos_por_cidade = df_pontos['cidade'].value_counts()
            st.markdown("**🏙️ Top Cidades com Mais Pontos:**")
            for cidade, count in pontos_por_cidade.head(3).items():
                st.markdown(f"• {cidade}: {count} ponto(s)")
        
        with col_stat2:
            # Horários mais comuns
            st.markdown("**🕐 Horários de Funcionamento:**")
            horarios = df_pontos['horario'].value_counts()
            for horario, count in horarios.head(3).items():
                st.markdown(f"• {horario}: {count} local(is)")
    
    with tab3:
        # Filtros
        st.markdown("#### 🔍 Filtrar Pontos")
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            cidades_disponiveis = sorted(set(p['cidade'] for p in pontos))
            cidade_filtro = st.multiselect(
                "Selecione as cidades:",
                options=cidades_disponiveis,
                default=cidades_disponiveis
            )
        
        with col_filter2:
            busca_nome = st.text_input("🔎 Buscar por nome:", "")
        
        # Filtrar pontos
        pontos_filtrados = [
            p for p in pontos 
            if p['cidade'] in cidade_filtro and 
            (busca_nome.lower() in p['nome'].lower() if busca_nome else True)
        ]
        
        # Agrupar por cidade
        pontos_por_cidade = {}
        for ponto in pontos_filtrados:
            cidade = ponto['cidade']
            if cidade not in pontos_por_cidade:
                pontos_por_cidade[cidade] = []
            pontos_por_cidade[cidade].append(ponto)
        
        # Mostrar pontos agrupados
        st.markdown(f"#### 📍 {len(pontos_filtrados)} Pontos Encontrados")
        
        for cidade, pontos_cidade in sorted(pontos_por_cidade.items()):
            with st.expander(f"🏙️ **{cidade}** ({len(pontos_cidade)} pontos)", expanded=True):
                for i, ponto in enumerate(pontos_cidade):
                    # Card para cada ponto
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff, #f8fff8); 
                                padding: 1.5rem; margin: 1rem 0; border-radius: 15px; 
                                border-left: 5px solid {material_info.get('color', '#3e8e41')}; 
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="margin: 0 0 0.5rem 0; color: #2d5a2d;">
                                    {material_emoji} {ponto['nome']}
                                </h4>
                                <p style="margin: 0.3rem 0; color: #555;">
                                    <strong>📍 Endereço:</strong> {ponto['endereco']}
                                </p>
                                <p style="margin: 0.3rem 0; color: #555;">
                                    <strong>🕐 Horário:</strong> {ponto['horario']}
                                </p>
                                <p style="margin: 0.3rem 0; color: #555;">
                                    <strong>📞 Telefone:</strong> {ponto.get('telefone', 'Não disponível')}
                                </p>
                            </div>
                            <div style="text-align: center; padding: 0.5rem;">
                                <a href="https://www.google.com/maps/search/?api=1&query={ponto['lat']},{ponto['lon']}" 
                                   target="_blank" 
                                   style="background: linear-gradient(45deg, #3e8e41, #28a745); 
                                          color: white; padding: 0.5rem 1rem; border-radius: 8px; 
                                          text-decoration: none; display: inline-block; 
                                          transition: all 0.3s ease;">
                                    🗺️ Ver no Maps
                                </a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Dicas e informações importantes
    st.markdown("---")
    st.markdown("### 💡 Informações Importantes")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
                    padding: 1.5rem; border-radius: 15px; border-left: 4px solid #2196f3;">
            <h4 style="margin: 0 0 0.5rem 0; color: #1565c0;">📞 Antes de Ir:</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Ligue para confirmar horários</li>
                <li>Verifique se aceitam o material</li>
                <li>Pergunte sobre quantidade máxima</li>
                <li>Confirme se precisa de cadastro</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); 
                    padding: 1.5rem; border-radius: 15px; border-left: 4px solid #ff9800;">
            <h4 style="margin: 0 0 0.5rem 0; color: #e65100;">📦 Preparação do Material:</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Limpe e seque o material</li>
                <li>Remova rótulos se possível</li>
                <li>Separe por tipo/categoria</li>
                <li>Embale de forma segura</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
def criar_grafico_estatisticas(material):
    pontos = PONTOS_COLETA.get(material, [])
    if not pontos:
        return None

    df = pd.DataFrame(pontos)
    cidades = df['cidade'].value_counts().head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=cidades.index,
            y=cidades.values,
            marker_color=CLASS_METADATA.get(material, {}).get('color', '#3e8e41')
        )
    ])
    fig.update_layout(
        title="Top Cidades com Pontos de Coleta",
        xaxis_title="Cidade",
        yaxis_title="Quantidade de Pontos",
        template="simple_white"
    )
    return fig

def mostrar_alertas_medalhas(novas_medalhas):
    """Mostra alertas de novas medalhas"""
    if novas_medalhas:
        st.balloons()
        for medalha_id in novas_medalhas:
            medalha = MEDALHAS[medalha_id]
            st.success(f"🏆 **Nova Medalha!** {medalha['emoji']} {medalha['nome']}")

def mostrar_sidebar():
    """Sidebar com navegação e info do usuário"""
    with st.sidebar:
        st.markdown("### 🎮 Navegação")
        
        # Botões de navegação
        paginas = {
            'Detector': '🔍 Detector IA',
            'Dashboard': '📊 Dashboard',
            'Ranking': '🏆 Ranking',
            'Mapa': '🗺️ Pontos de Coleta',
            'Loja': '🎁 RECOMPENSAS',
            'Sobre': 'ℹ️ Sobre'
        }
        
        for key, label in paginas.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
        
        st.markdown("---")
        
        # Info do usuário
        st.markdown("### 👤 Seu Perfil")
        user_data = st.session_state.user_data
        
        # Barra de progresso para próximo nível
        xp_atual = user_data['xp_total']
        xp_proximo_nivel = user_data['nivel_usuario'] * 100
        progresso = min(1.0, (xp_atual % 100) / 100)
        
        st.progress(progresso)
        st.markdown(f"**Nível {user_data['nivel_usuario']}** | XP: {xp_atual % 100}/100")
        
        # Estatísticas rápidas
        st.markdown(f"""
        **📊 Estatísticas:**
        - 🪙 EcoMoedas: {user_data['ecomoedas_total']}
        - 🎯 Detecções: {user_data['deteccoes_realizadas']}
        - 🏆 Medalhas: {len(user_data['medalhas_conquistadas'])}
        - 🌍 CO₂ Evitado: {user_data['impacto_total']['co2']:.1f}kg
        - 🎁 Recompensas: {len(user_data['recompensas_resgatadas'])} 
        """)
        
        st.markdown("---")
        
        # Medalhas recentes
        st.markdown("### 🏅 Medalhas Recentes")
        medalhas_usuario = user_data['medalhas_conquistadas']
        
        if medalhas_usuario:
            for medalha_id in medalhas_usuario[-3:]:  # Últimas 3
                medalha = MEDALHAS[medalha_id]
                st.markdown(f"{medalha['emoji']} **{medalha['nome']}**")
        else:
            st.info("Nenhuma medalha ainda. Faça sua primeira detecção!")
        
        st.markdown("---")
        
        # Configurações
        st.markdown("### ⚙️ Configurações")
        if st.button("🔄 Resetar Dados", help="Limpa todo o progresso"):
            st.session_state.user_data = {
                'ecomoedas_total': 0,
                'deteccoes_realizadas': 0,
                'historico_deteccoes': [],
                'medalhas_conquistadas': [],
                'impacto_total': {'co2': 0.0, 'energia': 0.0, 'agua': 0.0},
                'contadores_classe': {classe: 0 for classe in CLASSES},
                'streak_atual': 0,
                'nivel_usuario': 1,
                'xp_total': 0,
                'data_ultimo_acesso': datetime.now().isoformat(),
                'recompensas_resgatadas': []
            }
            st.success("✅ Dados resetados!")
            st.rerun()

# ================================================
# 📱 PÁGINAS DA APLICAÇÃO
# ================================================

def pagina_detector():
    """Página principal do detector"""
    st.markdown("## 🔍 Detector de Materiais")
    
    # Carregar modelo
    modelo = carregar_modelo()
    
    if modelo is None:
        st.error("❌ Não foi possível carregar o modelo. Verifique se o arquivo 'modelo_oikos.pt' está presente.")
        return
    
    # Layout em colunas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload de Imagem")
        
        # Área de upload
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Escolha uma imagem",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Arraste uma imagem aqui ou clique para selecionar"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mostrar imagem se carregada
        if uploaded_file is not None:
            try:
                imagem = Image.open(uploaded_file).convert("RGB")
                st.image(imagem, caption="Imagem carregada", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao carregar imagem: {str(e)}")
                return
        
        # Exemplos rápidos
        st.markdown("### 🖼️ Exemplos Rápidos")
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        if 'imagem_exemplo' not in st.session_state:
            st.session_state.imagem_exemplo = None
        with col_ex1:
            if st.button("📦 PAPELÃO", use_container_width=True):
                st.session_state.imagem_exemplo = "exemplos/papelao.png"
        with col_ex2:
            if st.button("🧴 PLÁSTICO", use_container_width=True):
                st.session_state.imagem_exemplo = "exemplos/plastico.png"
        with col_ex3:
            if st.button("🥫 METAL", use_container_width=True):
                st.session_state.imagem_exemplo = "exemplos/metal.png"
        if st.session_state.imagem_exemplo:
            try:
                imagem = Image.open(st.session_state.imagem_exemplo).convert("RGB")
                st.image(imagem, caption="🖼️ Exemplo carregado automaticamente", use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao carregar imagem de exemplo: {e}")

    with col2:
        st.markdown("### 🎯 Resultado da Análise")
        
        if uploaded_file is not None:
            # Fazer predição
            with st.spinner("🤖 Analisando com IA..."):
                resultado = fazer_predicao(modelo, imagem)
                
            if resultado[0] is not None:
                classe_predita, confianca, probabilidades, is_outlier = resultado
                
                if is_outlier:
                    st.markdown("""
                    <div class="custom-alert alert-warning">
                        <h3>🚫 Imagem Não Reconhecida</h3>
                        <p>Esta imagem não parece ser um resíduo conhecido.</p>
                        <strong>Dicas:</strong>
                        <ul>
                            <li>📸 Use boa iluminação</li>
                            <li>🎯 Foque em um objeto</li>
                            <li>🧹 Limpe o objeto</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Resultado válido
                    metadata = CLASS_METADATA[classe_predita]
                    ecomoeda_info = ECOMOEDA_SISTEMA[classe_predita]
                    
                    # Calcular EcoMoedas
                    multiplicador = 1.2 if confianca >= 0.9 else 0.8 if confianca < 0.7 else 1.0
                    ecomoedas_ganhas = int(ecomoeda_info['valor'] * multiplicador)
                    
                    # Nível de confiança
                    if confianca >= 0.8:
                        conf_class = "confidence-high"
                        conf_emoji = "🟢"
                        conf_texto = "Alta"
                    elif confianca >= 0.6:
                        conf_class = "confidence-medium"
                        conf_emoji = "🟡"
                        conf_texto = "Média"
                    else:
                        conf_class = "confidence-low"
                        conf_emoji = "🔴"
                        conf_texto = "Baixa"
                    
                    # Card de resultado
                    st.markdown(f"""
                    <div class="prediction-card">
                        <div style="text-align: center;">
                            <div style="font-size: 4rem; margin-bottom: 1rem;">{metadata['emoji']}</div>
                            <h2 style="margin: 0; color: {metadata['color']};">{metadata['name']}</h2>
                            <div class="confidence-indicator {conf_class}">
                                {conf_emoji} Confiança {conf_texto}: {confianca*100:.1f}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Status de reciclagem
                    if metadata['recyclable']:
                        st.markdown("""
                        <div class="custom-alert alert-success">
                            <h3>♻️ Material Reciclável!</h3>
                            <p>Excelente escolha para o meio ambiente!</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # EcoMoedas
                        st.markdown(f"""
                        <div class="ecomoeda-card">
                            <h2>🪙 +{ecomoedas_ganhas} EcoMoedas!</h2>
                            <p>Parabéns pela ação sustentável!</p>
                            <small>Multiplicador: {multiplicador:.1f}x</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botão de confirmação
                        if st.button("✅ Confirmar e Ganhar Recompensas", key="confirmar", use_container_width=True):
                            nivel_up, novas_medalhas = salvar_deteccao(classe_predita, confianca, ecomoedas_ganhas)
                            
                            if nivel_up:
                                st.success(f"🎉 Parabéns! Você subiu para o nível {st.session_state.user_data['nivel_usuario']}!")
                            
                            mostrar_alertas_medalhas(novas_medalhas)
                            st.rerun()
                    else:
                        st.markdown("""
                        <div class="custom-alert alert-warning">
                            <h3>🚫 Material Não Reciclável</h3>
                            <p>Este item não pode ser reciclado pelos métodos convencionais.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Dicas de descarte
                    st.markdown("### 💡 Dicas de Descarte")
                    for i, dica in enumerate(metadata['tips'], 1):
                        st.markdown(f"**{i}.** {dica}")
                    
                    # Curiosidade
                    st.info(f"🤓 **Curiosidade:** {metadata['curiosidade']}")
                    
                    # Gráfico de probabilidades
                    st.markdown("### 📊 Análise Detalhada")
                    fig = mostrar_grafico_probabilidades(probabilidades)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
                <div class="glass-card">
                    <h3>🚫 Imagem Não Reconhecida</h3>
                    <p>Esta imagem não parece ser um resíduo conhecido.</p>
                    <strong>Dicas:</strong>
                    <ul>
                        <li>📸 Use boa iluminação</li>
                        <li>🎯 Foque em um objeto</li>
                        <li>🧹 Limpe o objeto</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)


def pagina_dashboard():
    """Página do dashboard com estatísticas"""
    st.markdown("## 📊 Dashboard Pessoal")
    
    user_data = st.session_state.user_data
    
    # Métricas principais
    mostrar_metricas_usuario()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Detecções por Classe")
        
        if user_data['deteccoes_realizadas'] > 0:
            # Gráfico de pizza
            contadores = user_data['contadores_classe']
            classes_com_dados = {k: v for k, v in contadores.items() if v > 0}
            
            if classes_com_dados:
                df_classes = pd.DataFrame(list(classes_com_dados.items()), columns=['Classe', 'Quantidade'])
                df_classes['Nome'] = df_classes['Classe'].map(lambda x: CLASS_METADATA[x]['name'])
                df_classes['Emoji'] = df_classes['Classe'].map(lambda x: CLASS_METADATA[x]['emoji'])
                
                fig = px.pie(df_classes, values='Quantidade', names='Nome', title='Distribuição de Detecções')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma detecção realizada ainda.")
    
    with col2:
        st.markdown("### 🌍 Impacto Ambiental")
        
        impacto = user_data['impacto_total']
        
        # Métricas de impacto
        st.markdown(f"""
        <div class="glass-card">
            <div style="text-align: center;">
                <h3>🌱 CO₂ Evitado</h3>
                <div class="metric-value" style="color: #28a745;">{impacto['co2']:.1f} kg</div>
                <p>Equivale a plantar {impacto['co2']/22:.1f} árvores</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="text-align: center;">
                <h3>⚡ Energia Economizada</h3>
                <div class="metric-value" style="color: #ffc107;">{impacto['energia']:.1f} kWh</div>
                <p>Suficiente para {impacto['energia']*4:.0f} horas de TV</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="text-align: center;">
                <h3>💧 Água Poupada</h3>
                <div class="metric-value" style="color: #17a2b8;">{impacto['agua']:.1f} L</div>
                <p>Equivale a {impacto['agua']/2:.1f} garrafas d'água</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Histórico recente
    st.markdown("### 📈 Histórico Recente")
    
    if user_data['historico_deteccoes']:
        historico_recente = user_data['historico_deteccoes'][-10:]  # Últimos 10
        
        # Criar DataFrame
        df_historico = []
        for deteccao in historico_recente:
            df_historico.append({
                'Data': datetime.fromisoformat(deteccao['timestamp']).strftime('%d/%m %H:%M'),
                'Material': CLASS_METADATA[deteccao['classe']]['name'],
                'Emoji': CLASS_METADATA[deteccao['classe']]['emoji'],
                'Confiança': f"{deteccao['confianca']*100:.1f}%",
                'EcoMoedas': deteccao['ecomoedas']
            })
        
        df_historico = pd.DataFrame(df_historico)
        st.dataframe(df_historico, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum histórico disponível ainda.")

def pagina_ranking():
    """Página de ranking e medalhas"""
    st.markdown("## 🏆 Ranking e Medalhas")
    
    user_data = st.session_state.user_data
    
    # Seção de medalhas
    st.markdown("### 🏅 Suas Medalhas")
    
    medalhas_usuario = user_data['medalhas_conquistadas']
    
    if medalhas_usuario:
        # Mostrar medalhas em grid
        cols = st.columns(4)
        for i, medalha_id in enumerate(medalhas_usuario):
            medalha = MEDALHAS[medalha_id]
            with cols[i % 4]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{medalha['emoji']}</div>
                    <h4>{medalha['nome']}</h4>
                    <p><small>{medalha['desc']}</small></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Você ainda não possui medalhas. Faça detecções para conquistá-las!")
    
    # Medalhas disponíveis
    st.markdown("### 🎯 Medalhas Disponíveis")
    
    medalhas_nao_conquistadas = [m for m in MEDALHAS.keys() if m not in medalhas_usuario]
    
    if medalhas_nao_conquistadas:
        cols = st.columns(4)
        for i, medalha_id in enumerate(medalhas_nao_conquistadas):
            medalha = MEDALHAS[medalha_id]
            with cols[i % 4]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; opacity: 0.6;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem; filter: grayscale(100%);">{medalha['emoji']}</div>
                    <h4>{medalha['nome']}</h4>
                    <p><small>{medalha['desc']}</small></p>
                </div>
                """, unsafe_allow_html=True)
    
    # Estatísticas de progresso
    st.markdown("### 📊 Progresso para Medalhas")
    
    progresso_medalhas = {
        'Eco Iniciante': (user_data['ecomoedas_total'], 50),
        'Eco Guerreiro': (user_data['ecomoedas_total'], 200),
        'Eco Herói': (user_data['ecomoedas_total'], 500),
        'Especialista Plástico': (user_data['contadores_classe']['plastic'], 10),
        'Mestre Metal': (user_data['contadores_classe']['metal'], 10),
        'Guardião Vidro': (user_data['contadores_classe']['glass'], 10),
    }
    
    for medalha, (atual, meta) in progresso_medalhas.items():
        progresso = min(1.0, atual / meta)
        st.progress(progresso)
        st.markdown(f"**{medalha}**: {atual}/{meta} ({progresso*100:.1f}%)")

def pagina_recompensas():
    """Página de recompensas"""
    st.markdown("## 🎁 Loja de Recompensas")
    
    user_data = st.session_state.user_data
    
    # Mostrar saldo
    st.markdown(f"""
    <div class="ecomoeda-card">
        <h2>🪙 Saldo: {user_data['ecomoedas_total']} EcoMoedas</h2>
        <p>Use suas EcoMoedas para resgatar produtos sustentáveis!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para categorias
    tab1, tab2, tab3, tab4 = st.tabs(["👕 Roupas", "🛒 Cesta Básica", "📚 Material Escolar", "📜 Histórico"])
    
    with tab1:
        st.markdown("### 👕 Roupas Sustentáveis")
        cols = st.columns(3)
        
        for i, (item_id, item) in enumerate(RECOMPENSAS['roupas'].items()):
            with cols[i % 3]:
                pode_resgatar = user_data['ecomoedas_total'] >= item['custo']
                
                st.markdown(f"""
                <div class="reward-card {'disabled' if not pode_resgatar else ''}">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{item['emoji']}</div>
                    <h4>{item['nome']}</h4>
                    <p>{item['desc']}</p>
                    <h3>🪙 {item['custo']} EcoMoedas</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Resgatar {item['nome']}", key=f"roupas_{item_id}", disabled=not pode_resgatar):
                    if resgatar_recompensa(item_id, 'roupas'):
                        st.success(f"✅ {item['nome']} resgatado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
    
    with tab2:
        st.markdown("### 🛒 Cestas Básicas")
        cols = st.columns(3)
        
        for i, (item_id, item) in enumerate(RECOMPENSAS['cesta_basica'].items()):
            with cols[i % 3]:
                pode_resgatar = user_data['ecomoedas_total'] >= item['custo']
                
                st.markdown(f"""
                <div class="reward-card {'disabled' if not pode_resgatar else ''}">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{item['emoji']}</div>
                    <h4>{item['nome']}</h4>
                    <p>{item['desc']}</p>
                    <h3>🪙 {item['custo']} EcoMoedas</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Resgatar {item['nome']}", key=f"cesta_{item_id}", disabled=not pode_resgatar):
                    if resgatar_recompensa(item_id, 'cesta_basica'):
                        st.success(f"✅ {item['nome']} resgatado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
    
    with tab3:
        st.markdown("### 📚 Material Escolar")
        cols = st.columns(3)
        
        for i, (item_id, item) in enumerate(RECOMPENSAS['material_escolar'].items()):
            with cols[i % 3]:
                pode_resgatar = user_data['ecomoedas_total'] >= item['custo']
                
                st.markdown(f"""
                <div class="reward-card {'disabled' if not pode_resgatar else ''}">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{item['emoji']}</div>
                    <h4>{item['nome']}</h4>
                    <p>{item['desc']}</p>
                    <h3>🪙 {item['custo']} EcoMoedas</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Resgatar {item['nome']}", key=f"material_{item_id}", disabled=not pode_resgatar):
                    if resgatar_recompensa(item_id, 'material_escolar'):
                        st.success(f"✅ {item['nome']} resgatado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
    
    with tab4:
        st.markdown("### 📜 Histórico de Resgates")
        
        if user_data['recompensas_resgatadas']:
            # Criar DataFrame
            df_historico = []
            for resgate in user_data['recompensas_resgatadas']:
                df_historico.append({
                    'Data': datetime.fromisoformat(resgate['timestamp']).strftime('%d/%m/%Y %H:%M'),
                    'Recompensa': resgate['nome'],
                    'Categoria': resgate['categoria'].replace('_', ' ').title(),
                    'Custo': f"🪙 {resgate['custo']}"
                })
            
            df_historico = pd.DataFrame(df_historico)
            st.dataframe(df_historico, use_container_width=True, hide_index=True)
            
            # Total gasto
            total_gasto = sum(r['custo'] for r in user_data['recompensas_resgatadas'])
            st.markdown(f"""
            <div class="glass-card">
                <h3>Total de EcoMoedas Gastas: 🪙 {total_gasto}</h3>
                <p>Você já resgatou {len(user_data['recompensas_resgatadas'])} recompensas!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Você ainda não resgatou nenhuma recompensa. Explore a loja!")
    
    # Dicas de economia
    st.markdown("### 💡 Dicas para Ganhar Mais EcoMoedas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4>🎯 Precisão Alta</h4>
            <p>Detecções com confiança acima de 90% ganham 20% mais EcoMoedas!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4>🥫 Materiais Raros</h4>
            <p>Metal e vidro valem mais EcoMoedas por serem mais valiosos!</p>
        </div>
        """, unsafe_allow_html=True)

def pagina_mapa():
    """Página com mapa de pontos de coleta"""
    st.markdown("## 🗺️ Pontos de Coleta")
    
    # Seletor de material
    material_selecionado = st.selectbox(
        "🔎 Selecione o material:",
        options=list(PONTOS_COLETA.keys()),
        format_func=lambda x: f"{CLASS_METADATA[x]['emoji']} {CLASS_METADATA[x]['name']}"
    )
    
    # Informações do material
    metadata = CLASS_METADATA[material_selecionado]
    
    st.markdown(f"""
    <div class="glass-card">
        <h3>{metadata['emoji']} Pontos de Coleta para {metadata['name']}</h3>
        <p>Encontre os locais mais próximos para descartar seu material de forma sustentável.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Criar e mostrar mapa
    mapa = criar_mapa_interativo(PONTOS_COLETA[material_selecionado])
    
    if mapa:
        st.pydeck_chart(mapa, use_container_width=True)
        
        # Lista de pontos
        st.markdown("### 📍 Lista de Pontos")
        pontos = PONTOS_COLETA[material_selecionado]
        
        for ponto in pontos:
            st.markdown(f"""
            <div class="glass-card">
                <h4>{ponto['nome']}</h4>
                <p>📍 {ponto['cidade']}</p>
                <p>🗺️ Lat: {ponto['lat']:.4f}, lon: {ponto['lon']:.4f}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Nenhum ponto de coleta disponível para este material.")

def pagina_sobre():
    """Página sobre o projeto"""
    st.markdown("## ℹ️ Sobre o EcoDetector v2.0")
    
    st.markdown("""
    <div class="glass-card">
        <h3>🌱 Missão</h3>
        <p>Transformar a reciclagem em uma experiência divertida e recompensadora, 
        promovendo a consciência ambiental através da gamificação e inteligência artificial.</p>
        
        <h3>🚀 Tecnologia</h3>
        <ul>
            <li><strong>IA:</strong> EfficientNet-B0 treinado para classificação de resíduos</li>
            <li><strong>Framework:</strong> PyTorch para deep learning</li>
            <li><strong>Interface:</strong> Streamlit para aplicação web</li>
            <li><strong>Visualização:</strong> Plotly para gráficos interativos</li>
            <li><strong>Mapas:</strong> Pydeck para visualização geoespacial</li>
        </ul>
        
        <h3>🏆 Gamificação</h3>
        <ul>
            <li><strong>EcoMoedas:</strong> Sistema de recompensas por detecções</li>
            <li><strong>Medalhas:</strong> Conquistas por marcos alcançados</li>
            <li><strong>Níveis:</strong> Progressão baseada em XP</li>
            <li><strong>Impacto:</strong> Visualização do benefício ambiental</li>
        </ul>
        
        <h3>🎯 Funcionalidades</h3>
        <ul>
            <li>Detecção automática de 6 tipos de materiais</li>
            <li>Sistema de confiança e detecção de outliers</li>
            <li>Dashboard pessoal com estatísticas</li>
            <li>Mapa de pontos de coleta no RS</li>
            <li>Ranking e sistema de medalhas</li>
            <li>Dicas personalizadas de reciclagem</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas do modelo
    st.markdown("### 📊 Estatísticas do Modelo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="modern-metric">
            <div class="metric-value">6</div>
            <div class="metric-label">Classes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-metric">
            <div class="metric-value">95%</div>
            <div class="metric-label">Acurácia</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="modern-metric">
            <div class="metric-value">224x224</div>
            <div class="metric-label">Resolução</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Créditos
    st.markdown("""
    <div class="glass-card">
        <h3>👥 Créditos</h3>
        <p>Desenvolvido com ❤️ para um futuro mais sustentável.</p>
        <p><strong>Versão:</strong> 2.0.0</p>
        <p><strong>Última atualização:</strong> 2025</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================
# 🚀 APLICAÇÃO PRINCIPAL
# ================================================
def main():
    """Função principal da aplicação"""
    # Carregar CSS
    load_css()
    
    # Inicializar sessão
    inicializar_sessao()
    
    # Mostrar sidebar
    mostrar_sidebar()
    
    # Header principal
    criar_header()
    
    # Roteamento de páginas
    pagina_atual = st.session_state.current_page
    
    if pagina_atual == 'Detector':
        pagina_detector()
    elif pagina_atual == 'Dashboard':
        pagina_dashboard()
    elif pagina_atual == 'Ranking':
        pagina_ranking()
    elif pagina_atual == 'Loja': 
        pagina_recompensas() 
    elif pagina_atual == 'Mapa':
        material = st.selectbox("Selecione o material:", list(CLASS_METADATA.keys()))
        mostrar_secao_mapa_melhorada(material)
    elif pagina_atual == 'Sobre':
        pagina_sobre()
  
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>🌱 EcoDetector v2.0 - Sistema Inteligente de Reciclagem</p>
        <p><small>Transformando o mundo, uma detecção por vez! 🌍</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
