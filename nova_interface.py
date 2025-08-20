import streamlit as st
import random
from datetime import datetime, timedelta

import os, base64
import time
import pandas as pd
import numpy as np
import base64

# ========================= CONFIGURAÇÃO INICIAL =========================
st.set_page_config(
    page_title="EcoSphere - Rede Social Sustentável",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================= BANCO DE DADOS SIMULADO =========================
class Database:
    """Sistema de banco de dados simulado com persistência na sessão"""
    
    @staticmethod
    def init_database():
        """Inicializa todos os dados necessários na sessão"""
        # Usuários
        if 'db_users' not in st.session_state:
            st.session_state.db_users = {
                'nicolasfranca': {
                    'password': 'demo123',
                    'name': 'Nicolas França',
                    'username': 'nicolasfranca',
                    'avatar': 'my_Face.png',  # Caminho da imagem
                    'avatar_url': None,
                    'level': 7,
                    'ecoins': 1250,
                    'xp': 3450,
                    'bio': 'Apaixonado por sustentabilidade e tecnologia verde 🌱',
                    'location': 'São Paulo, Brasil',
                    'joined': datetime(2024, 1, 15),
                    'followers': 342,
                    'following': 289,
                    'posts_count': 47,
                    'badges': ['eco_warrior', 'recycler_pro', 'community_leader'],
                    'stats': {
                        'total_recycled': 127.5,
                        'trees_saved': 8,
                        'water_saved': 3450,
                        'energy_saved': 892,
                        'co2_reduced': 234.5
                    },
                    'verified': True
                }
            }
        
        # Posts do feed
        if 'db_posts' not in st.session_state:
            st.session_state.db_posts = [
                {
                    'id': 'post_001',
                    'author': 'Maria Silva',
                    'author_username': 'mariasilva',
                    'author_avatar': '👩',
                    'author_level': 12,
                    'author_verified': True,
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'content': '🎉 Completei meu 100º dia consecutivo reciclando! Cada pequena ação conta para um futuro mais verde. Hoje reciclei 15kg de materiais diversos e ajudei 3 vizinhos a começarem sua jornada sustentável.',
                    'image': 'recycling_achievement.jpg',
                    'likes': 234,
                    'comments': [
                        {
                            'author': 'João Pedro',
                            'avatar': '👨‍💼',
                            'text': 'Parabéns Maria! Você é uma verdadeira inspiração! 💚',
                            'timestamp': datetime.now() - timedelta(hours=1)
                        },
                        {
                            'author': 'Ana Costa',
                            'avatar': '👩‍🎨',
                            'text': 'Incrível! Como você mantém a motivação todos os dias?',
                            'timestamp': datetime.now() - timedelta(minutes=30)
                        }
                    ],
                    'shares': 45,
                    'user_liked': False,
                    'user_saved': False,
                    'tags': ['#EcoWarrior', '#100DaysChallenge', '#Sustentabilidade']
                },
                {
                    'id': 'post_002',
                    'author': 'Pedro Santos',
                    'author_username': 'pedrosantos',
                    'author_avatar': '👨',
                    'author_level': 9,
                    'author_verified': False,
                    'timestamp': datetime.now() - timedelta(hours=5),
                    'content': 'Hoje organizei um mutirão de limpeza na Praia de Copacabana! 🏖️ Coletamos mais de 50kg de resíduos em apenas 3 horas. Próximo mutirão será sábado que vem, quem topa?',
                    'image': 'beach_cleanup.jpg',
                    'likes': 567,
                    'comments': [
                        {
                            'author': 'Marina Oliveira',
                            'avatar': '👩‍💻',
                            'text': 'Eu vou! Posso levar meus amigos?',
                            'timestamp': datetime.now() - timedelta(hours=4)
                        }
                    ],
                    'shares': 112,
                    'user_liked': True,
                    'user_saved': True,
                    'tags': ['#MutirãoEcológico', '#PraiasLimpas']
                },
                {
                    'id': 'post_003',
                    'author': 'EcoTips Daily',
                    'author_username': 'ecotipsdaily',
                    'author_avatar': '💡',
                    'author_level': 15,
                    'author_verified': True,
                    'timestamp': datetime.now() - timedelta(hours=8),
                    'content': '💡 DICA DO DIA: Você sabia que uma única árvore pode absorver até 22kg de CO2 por ano? Imagine o impacto de plantar 10, 100 ou 1000 árvores! 🌳',
                    'image': None,
                    'likes': 892,
                    'comments': [],
                    'shares': 234,
                    'user_liked': False,
                    'user_saved': False,
                    'tags': ['#DicaSustentável', '#MeioAmbiente']
                },
                {
                    'id': 'post_004',
                    'author': 'Ana Beatriz',
                    'author_username': 'anabeatriz',
                    'author_avatar': '👩‍🌾',
                    'author_level': 8,
                    'author_verified': False,
                    'timestamp': datetime.now() - timedelta(days=1),
                    'content': 'Transformei minha varanda em uma horta urbana! 🥬🥕 Economizando dinheiro e reduzindo a pegada de carbono. Quem quer dicas de como começar a sua?',
                    'image': 'urban_garden.jpg',
                    'likes': 445,
                    'comments': [],
                    'shares': 67,
                    'user_liked': False,
                    'user_saved': True,
                    'tags': ['#HortaUrbana', '#VidaSustentável']
                }
            ]
        
        # Stories
        if 'db_stories' not in st.session_state:
            st.session_state.db_stories = [
                {'id': 1, 'author': 'Adicionar', 'avatar': '➕', 'is_user': True, 'has_new': False},
                {'id': 2, 'author': 'Ana', 'avatar': '👩‍🦰', 'is_user': False, 'has_new': True},
                {'id': 3, 'author': 'Carlos', 'avatar': '👨‍💼', 'is_user': False, 'has_new': True},
                {'id': 4, 'author': 'EcoTips', 'avatar': '💡', 'is_user': False, 'has_new': False},
                {'id': 5, 'author': 'Marina', 'avatar': '👩‍🎨', 'is_user': False, 'has_new': True}
            ]
        
        # Trending topics
        if 'db_trending' not in st.session_state:
            st.session_state.db_trending = [
                {'rank': 1, 'tag': '#DiaDoMeioAmbiente', 'posts': '12.3K', 'trend': 'up'},
                {'rank': 2, 'tag': '#ReciclagemCriativa', 'posts': '8.7K', 'trend': 'up'},
                {'rank': 3, 'tag': '#HortaEmCasa', 'posts': '6.2K', 'trend': 'same'},
                {'rank': 4, 'tag': '#LixoZero', 'posts': '5.1K', 'trend': 'down'}
            ]
        
        # Sugestões de conexão
        if 'db_suggestions' not in st.session_state:
            st.session_state.db_suggestions = [
                {
                    'name': 'Laura Mendes',
                    'username': 'lauramendes',
                    'avatar': '👩‍⚕️',
                    'bio': 'Médica e ativista ambiental',
                    'followers': 2300,
                    'verified': True
                },
                {
                    'name': 'Ricardo Alves',
                    'username': 'ricardo_eco',
                    'avatar': '👨‍🏭',
                    'bio': 'Engenheiro de energias renováveis',
                    'followers': 1800,
                    'verified': False
                }
            ]
        
        # Desafios
        if 'db_challenges' not in st.session_state:
            st.session_state.db_challenges = [
                {'name': 'Reciclador Diário', 'desc': 'Recicle 5 itens', 'progress': 3, 'total': 5, 'reward': 50, 'icon': '♻️'},
                {'name': 'Social Eco', 'desc': 'Interaja com 3 posts', 'progress': 1, 'total': 3, 'reward': 30, 'icon': '💬'}
            ]
        
        # Notificações
        if 'notifications' not in st.session_state:
            st.session_state.notifications = [
                {'type': 'like', 'text': 'Maria Silva curtiu seu post', 'time': '5 min', 'unread': True},
                {'type': 'comment', 'text': 'João comentou: "Excelente iniciativa!"', 'time': '15 min', 'unread': True},
                {'type': 'achievement', 'text': 'Nova conquista desbloqueada!', 'time': '1h', 'unread': False},
                {'type': 'follow', 'text': 'Ana Costa começou a seguir você', 'time': '2h', 'unread': True}
            ]
        
        # Estado da navegação
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'feed'
        
        # Estado da busca
        if 'search_query' not in st.session_state:
            st.session_state.search_query = ''
        
        # Estado do dropdown de notificações
        if 'show_notifications' not in st.session_state:
            st.session_state.show_notifications = False

# ========================= ESTILOS CSS ULTRA-MODERNOS =========================
def load_ultra_modern_css():
    """Carrega estilos CSS ultra-modernos com navbar profissional"""
    st.markdown("""
    <style>
        /* ===== Importação de Fontes ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* ===== Variáveis de Design System ===== */
        :root {
            /* Cores Principais */
            --primary-green: #27ae60;
            --primary-green-hover: #229954;
            --primary-blue: #3498db;
            --primary-blue-hover: #2980b9;
            --dark-gray: #2c3e50;
            --medium-gray: #7f8c8d;
            --light-gray: #ecf0f1;
            --lighter-gray: #f8f9fa;
            --white: #ffffff;
            --background: #f5f6fa;
            
            /* Cores de Estado */
            --success: #27ae60;
            --warning: #f39c12;
            --error: #e74c3c;
            --info: #3498db;
            
            /* Sombras */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.08);
            --shadow-xl: 0 8px 16px rgba(0, 0, 0, 0.12);
            --shadow-navbar: 0 2px 8px rgba(0, 0, 0, 0.08);
            
            /* Bordas */
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-2xl: 24px;
            --radius-full: 9999px;
            
            /* Espaçamentos */
            --spacing-xs: 4px;
            --spacing-sm: 8px;
            --spacing-md: 16px;
            --spacing-lg: 24px;
            --spacing-xl: 32px;
            --spacing-2xl: 48px;
            
            /* Transições */
            --transition-fast: all 0.1s ease;
            --transition-base: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            
            /* Navbar */
            --navbar-height: 64px;
        }
        
        /* ===== Reset e Base ===== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            box-sizing: border-box;
        }
        
        .stApp {
            background: var(--background);
        }
        
        .block-container {
            padding-top: calc(var(--navbar-height) + 20px) !important;
            max-width: 1400px !important;
            margin: 0 auto;
        }
        
        /* ===== Ocultar elementos padrão do Streamlit ===== */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ===== Navbar Ultra-Moderno ===== */
        .modern-navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--navbar-height);
            background: var(--white);
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
            box-shadow: var(--shadow-navbar);
            z-index: 999;
            display: flex;
            align-items: center;
            padding: 0 24px;
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.98);
        }
        
        .navbar-container {
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 48px;
        }
        
        /* Logo Section */
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: var(--dark-gray);
            font-weight: 700;
            font-size: 20px;
            cursor: pointer;
            transition: var(--transition-base);
        }
        
        .navbar-brand:hover {
            color: var(--primary-green);
        }
        
        .navbar-logo {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-md);
            background: linear-gradient(135deg, var(--primary-green), var(--primary-blue));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        
        /* Navigation Menu */
        .navbar-nav {
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            justify-content: center;
        }
        
        .nav-item {
            position: relative;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: var(--radius-md);
            color: var(--medium-gray);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: var(--transition-base);
            cursor: pointer;
            background: transparent;
            border: none;
        }
        
        .nav-item:hover {
            color: var(--dark-gray);
            background: var(--lighter-gray);
        }
        
        .nav-item.active {
            color: var(--primary-green);
            background: rgba(39, 174, 96, 0.1);
        }
        
        .nav-item.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 16px;
            right: 16px;
            height: 2px;
            background: var(--primary-green);
            border-radius: var(--radius-full);
        }
        
        .nav-icon {
            font-size: 18px;
        }
        
        .nav-text {
            font-size: 14px;
        }
        
        /* Search Bar */
        .navbar-search {
            position: relative;
            display: flex;
            align-items: center;
            background: var(--lighter-gray);
            border-radius: var(--radius-full);
            padding: 0 16px;
            height: 40px;
            min-width: 280px;
            transition: var(--transition-base);
            border: 2px solid transparent;
        }
        
        .navbar-search:hover {
            background: var(--light-gray);
        }
        
        .navbar-search:focus-within {
            background: var(--white);
            border-color: var(--primary-green);
            box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
        }
        
        .search-icon {
            color: var(--medium-gray);
            margin-right: 8px;
            font-size: 16px;
        }
        
        .search-input {
            background: transparent;
            border: none;
            outline: none;
            flex: 1;
            font-size: 14px;
            color: var(--dark-gray);
            placeholder-color: var(--medium-gray);
        }
        
        .search-input::placeholder {
            color: var(--medium-gray);
        }
        
        /* Navbar Actions */
        .navbar-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .navbar-btn {
            position: relative;
            width: 40px;
            height: 40px;
            border-radius: var(--radius-full);
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            color: var(--medium-gray);
            border: none;
            cursor: pointer;
            transition: var(--transition-base);
            font-size: 20px;
        }
        
        .navbar-btn:hover {
            background: var(--lighter-gray);
            color: var(--dark-gray);
        }
        
        .navbar-btn.active {
            background: var(--lighter-gray);
            color: var(--primary-green);
        }
        
        /* Notification Badge */
        .notification-dot {
            position: absolute;
            top: 8px;
            right: 8px;
            width: 8px;
            height: 8px;
            background: var(--error);
            border-radius: var(--radius-full);
            border: 2px solid var(--white);
            animation: pulse 2s infinite;
        }
        
        .notification-count {
            position: absolute;
            top: 4px;
            right: 4px;
            background: var(--error);
            color: var(--white);
            border-radius: var(--radius-full);
            padding: 2px 6px;
            font-size: 11px;
            font-weight: 600;
            min-width: 18px;
            text-align: center;
            border: 2px solid var(--white);
        }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        /* Profile Avatar */
        .navbar-avatar {
            width: 32px;
            height: 32px;
            border-radius: var(--radius-full);
            background: linear-gradient(135deg, var(--primary-green), var(--primary-blue));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            cursor: pointer;
            transition: var(--transition-base);
            border: 2px solid transparent;
        }
        
        .navbar-avatar:hover {
            transform: scale(1.05);
            border-color: var(--primary-green);
        }
        
        /* Dropdown Menu */
        .dropdown-menu {
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            background: var(--white);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            border: 1px solid rgba(0, 0, 0, 0.08);
            min-width: 320px;
            max-height: 480px;
            overflow-y: auto;
            z-index: 1000;
            animation: slideDown 0.2s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .dropdown-header {
            padding: 16px;
            border-bottom: 1px solid var(--light-gray);
            font-weight: 600;
            color: var(--dark-gray);
        }
        
        .notification-item {
            display: flex;
            align-items: flex-start;
            padding: 12px 16px;
            border-bottom: 1px solid var(--lighter-gray);
            cursor: pointer;
            transition: var(--transition-base);
        }
        
        .notification-item:hover {
            background: var(--lighter-gray);
        }
        
        .notification-item.unread {
            background: rgba(52, 152, 219, 0.05);
        }
        
        .notification-icon {
            width: 36px;
            height: 36px;
            border-radius: var(--radius-full);
            background: var(--lighter-gray);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            flex-shrink: 0;
        }
        
        .notification-content {
            flex: 1;
        }
        
        .notification-text {
            font-size: 14px;
            color: var(--dark-gray);
            margin-bottom: 4px;
        }
        
        .notification-time {
            font-size: 12px;
            color: var(--medium-gray);
        }
        
        /* ===== Cards Clean ===== */
        .clean-card {
            background: var(--white);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg);
            box-shadow: var(--shadow-md);
            transition: var(--transition-base);
            margin-bottom: var(--spacing-md);
            border: 1px solid rgba(0, 0, 0, 0.04);
        }
        
        .clean-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        /* ===== Post Card ===== */
        .post-card {
            background: var(--white);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin-bottom: var(--spacing-lg);
            transition: var(--transition-base);
            border: 1px solid rgba(0, 0, 0, 0.04);
            overflow: hidden;
        }
        
        .post-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-1px);
        }
        
        .post-header {
            padding: var(--spacing-lg);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .post-author {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }
        
        .post-author-avatar {
            width: 48px;
            height: 48px;
            border-radius: var(--radius-full);
            background: linear-gradient(135deg, var(--light-gray), var(--lighter-gray));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .post-author-info {
            display: flex;
            flex-direction: column;
        }
        
        .post-author-name {
            font-size: 15px;
            font-weight: 600;
            color: var(--dark-gray);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .verified-badge {
            color: var(--primary-blue);
            font-size: 14px;
        }
        
        .post-author-meta {
            font-size: 13px;
            color: var(--medium-gray);
        }
        
        .post-content {
            padding: 0 var(--spacing-lg) var(--spacing-lg);
            color: var(--dark-gray);
            line-height: 1.6;
            font-size: 15px;
        }
        
        .post-image-placeholder {
            width: 100%;
            height: 300px;
            background: linear-gradient(135deg, var(--lighter-gray), var(--light-gray));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: var(--medium-gray);
        }
        
        .post-stats {
            padding: var(--spacing-md) var(--spacing-lg);
            display: flex;
            gap: var(--spacing-lg);
            font-size: 14px;
            color: var(--medium-gray);
            border-top: 1px solid var(--lighter-gray);
            border-bottom: 1px solid var(--lighter-gray);
        }
        
        .post-stat {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .post-actions {
            padding: var(--spacing-sm);
            display: flex;
            justify-content: space-around;
        }
        
        .post-action-btn {
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            padding: var(--spacing-sm) var(--spacing-lg);
            border-radius: var(--radius-md);
            background: transparent;
            border: none;
            color: var(--medium-gray);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-base);
        }
        
        .post-action-btn:hover {
            background: var(--lighter-gray);
            color: var(--primary-green);
        }
        
        .post-action-btn.liked {
            color: var(--error);
        }
        
        .post-action-btn.saved {
            color: var(--warning);
        }
        
        /* ===== Stories Section ===== */
        .stories-container {
            display: flex;
            gap: var(--spacing-md);
            padding: var(--spacing-md) 0;
            overflow-x: auto;
            scrollbar-width: none;
        }
        
        .stories-container::-webkit-scrollbar {
            display: none;
        }
        
        .story-item {
            min-width: 72px;
            text-align: center;
            cursor: pointer;
            transition: var(--transition-base);
        }
        
        .story-item:hover {
            transform: scale(1.05);
        }
        
        .story-avatar {
            width: 64px;
            height: 64px;
            border-radius: var(--radius-full);
            padding: 3px;
            background: linear-gradient(135deg, var(--primary-green), var(--primary-blue));
            margin-bottom: 4px;
            transition: var(--transition-base);
        }
        
        .story-avatar.no-story {
            background: var(--light-gray);
        }
        
        .story-avatar:hover {
            transform: rotate(5deg) scale(1.05);
        }
        
        .story-avatar-inner {
            width: 100%;
            height: 100%;
            border-radius: var(--radius-full);
            background: var(--white);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            border: 2px solid var(--white);
        }
        
        .story-name {
            font-size: 12px;
            color: var(--medium-gray);
            font-weight: 500;
        }
        
        /* ===== Utilities ===== */
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--dark-gray);
            margin-bottom: var(--spacing-md);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .widget-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--dark-gray);
            margin-bottom: var(--spacing-md);
            padding-bottom: var(--spacing-sm);
            border-bottom: 2px solid var(--lighter-gray);
        }
        
        /* ===== Responsive ===== */
        @media (max-width: 768px) {
            .navbar-nav {
                display: none;
            }
            
            .navbar-search {
                display: none;
            }
            
            .navbar-container {
                gap: 16px;
            }
            
            .block-container {
                padding: calc(var(--navbar-height) + 10px) 10px 10px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ========================= COMPONENTES UI APRIMORADOS =========================
class UIComponents:
    """Componentes de UI com navbar ultra-moderno"""
    
    @staticmethod
    def render_modern_navbar():
        """Renderiza navbar ultra-moderno estilo grandes apps"""
        current_page = st.session_state.get('current_page', 'feed')
        unread_count = sum(1 for n in st.session_state.notifications if n.get('unread', False))

        # HTML do Navbar
        html_navbar = f'''
        <div class="modern-navbar">
            <div class="navbar-container">
                <a class="navbar-brand" href="#">
                    <span class="navbar-logo">🌍</span>
                    EcoSphere
                </a>
                <!-- Navigation Menu -->
                <nav class="navbar-nav">
                    <button class="nav-item {'active' if current_page == 'feed' else ''}" onclick="window.location.hash='feed'">
                        <span class="nav-icon">🏠</span>
                        <span class="nav-text">Feed</span>
                    </button>
                    <button class="nav-item {'active' if current_page == 'education' else ''}" onclick="window.location.hash='education'">
                        <span class="nav-icon">📚</span>
                        <span class="nav-text">Educação</span>
                    </button>
                    <button class="nav-item {'active' if current_page == 'challenges' else ''}" onclick="window.location.hash='challenges'">
                        <span class="nav-icon">🏆</span>
                        <span class="nav-text">Desafios</span>
                    </button>
                    <button class="nav-item {'active' if current_page == 'marketplace' else ''}" onclick="window.location.hash='marketplace'">
                        <span class="nav-icon">🛍️</span>
                        <span class="nav-text">Market</span>
                    </button>
                    <button class="nav-item {'active' if current_page == 'collection' else ''}" onclick="window.location.hash='collection'">
                        <span class="nav-icon">📍</span>
                        <span class="nav-text">Coleta</span>
                    </button>
                </nav>
                <!-- Actions -->
                <div class="navbar-actions">
                    <!-- Search Bar -->
                    <div class="navbar-search">
                        <span class="search-icon">🔍</span>
                        <input type="text" class="search-input" placeholder="Buscar no EcoSphere..." />
                    </div>
                    <!-- Notifications -->
                    <button class="navbar-btn" id="notif-btn">
                        <span>🔔</span>
                        <span class="notification-count">{unread_count}</span>
                    </button>
                    <!-- Profile -->
                    <div class="navbar-avatar">
                        🌱
                    </div>
                </div>
            </div>
        </div>
        '''
        st.markdown(html_navbar, unsafe_allow_html=True)
    # (JavaScript opcional pode ser adicionado aqui se necessário)
    
    @staticmethod
    def render_profile_widget():
        """Widget de perfil limpo e moderno"""
        user = st.session_state.user_data
        
        st.markdown('<div class="widget-title">👤 Meu Perfil</div>', unsafe_allow_html=True)
        
        # Avatar centralizado - sempre usa my_Face.png para o usuário nicolasfranca
        avatar_html = ""
        username = user.get('username', '')
        
        # Força o uso da foto my_Face.png para nicolasfranca
        if username == 'nicolasfranca':
            avatar_file = "fotos/my_Face.png"
            try:
                if os.path.exists(avatar_file):
                    with open(avatar_file, "rb") as img_file:
                        avatar_b64 = base64.b64encode(img_file.read()).decode()
                    avatar_html = f"<img src='data:image/png;base64,{avatar_b64}' style='width:96px;height:96px;border-radius:50%;object-fit:cover;margin-bottom:12px;border:3px solid #27ae60;'>"
                else:
                    avatar_html = "<div style='font-size:64px;margin-bottom:12px;'>👤</div>"
            except Exception:
                avatar_html = "<div style='font-size:64px;margin-bottom:12px;'>👤</div>"
        else:
            # Para outros usuários, usa o avatar padrão
            avatar_html = f"<div style='font-size:64px;margin-bottom:12px;'>{user.get('avatar','👤')}</div>"
        st.markdown(f"""
        <div style='text-align: center; margin: 24px 0;'>
            {avatar_html}
            <div style='font-size: 18px; font-weight: 600; color: #2c3e50;'>{user['name']}</div>
            <div style='font-size: 14px; color: #7f8c8d;'>@{user['username']} • Nível {user['level']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Estatísticas em grid
        cols = st.columns(3)
        stats = [
            (f"{user['followers']}", "Seguidores"),
            (f"{user['following']}", "Seguindo"),
            (f"{user['posts_count']}", "Posts")
        ]
        
        for col, (value, label) in zip(cols, stats):
            with col:
                st.markdown(f"""
                <div style='text-align: center;'>
                    <div style='font-size: 20px; font-weight: 600; color: #2c3e50;'>{value}</div>
                    <div style='font-size: 12px; color: #7f8c8d;'>{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Bio
        st.markdown(f"""
        <div style='margin-top: 20px; padding: 12px; background: #f8f9fa; border-radius: 8px;'>
            <p style='margin: 0; color: #7f8c8d; font-size: 14px; font-style: italic;'>{user['bio']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_challenges_widget():
        """Widget de desafios minimalista"""
        st.markdown('<div class="widget-title">🎯 Desafios de Hoje</div>', unsafe_allow_html=True)
        
        for challenge in st.session_state.db_challenges:
            progress = challenge['progress'] / challenge['total']
            
            st.markdown(f"""
            <div style='margin-bottom: 16px; padding: 12px; background: #f8f9fa; border-radius: 8px; 
                        border-left: 3px solid #27ae60;'>
                <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px;'>
                    <span style='font-size: 20px;'>{challenge['icon']}</span>
                    <span style='font-weight: 600; color: #2c3e50; font-size: 14px;'>{challenge['name']}</span>
                </div>
                <div style='font-size: 12px; color: #7f8c8d; margin-bottom: 8px;'>{challenge['desc']}</div>
                <div style='background: #ecf0f1; border-radius: 4px; height: 6px; overflow: hidden;'>
                    <div style='background: #27ae60; height: 100%; width: {progress*100}%; transition: width 0.3s;'></div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 6px;'>
                    <span style='font-size: 11px; color: #7f8c8d;'>{challenge['progress']}/{challenge['total']}</span>
                    <span style='font-size: 11px; color: #27ae60; font-weight: 600;'>🪙 {challenge['reward']} pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_stories():
        """Seção de stories moderna"""
        st.markdown('<div class="section-title">📱 Stories</div>', unsafe_allow_html=True)
        
        story_cols = st.columns(len(st.session_state.db_stories))
        
        for col, story in zip(story_cols, st.session_state.db_stories):
            with col:
                border_style = "story-avatar" if story['has_new'] else "story-avatar no-story"
                
                st.markdown(f"""
                <div class="story-item">
                    <div class="{border_style}">
                        <div class="story-avatar-inner">{story['avatar']}</div>
                    </div>
                    <div class="story-name">{story['author']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button('', key=f"story_{story['id']}", help=story['author']):
                    if story['is_user']:
                        st.toast("📸 Adicionar story")
                    else:
                        st.toast(f"Vendo story de {story['author']}")
    
    @staticmethod
    def render_create_post():
        """Criar post com design moderno"""
        st.markdown('<div class="section-title">✍️ Criar Publicação</div>', unsafe_allow_html=True)
        
        with st.container():
            cols = st.columns([1, 11])
            with cols[0]:
                # Avatar do usuário na seção de criar post
                username = st.session_state.user_data.get('username', '')
                if username == 'nicolasfranca':
                    avatar_file = "fotos/my_Face.png"
                    try:
                        if os.path.exists(avatar_file):
                            with open(avatar_file, "rb") as img_file:
                                avatar_b64 = base64.b64encode(img_file.read()).decode()
                            st.markdown(f"""
                            <img src='data:image/png;base64,{avatar_b64}' style='width:40px;height:40px;border-radius:50%;object-fit:cover;margin-top:8px;'>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style='font-size: 40px; margin-top: 8px;'>👤</div>
                            """, unsafe_allow_html=True)
                    except Exception:
                        st.markdown(f"""
                        <div style='font-size: 40px; margin-top: 8px;'>👤</div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='font-size: 40px; margin-top: 8px;'>{st.session_state.user_data.get('avatar','👤')}</div>
                    """, unsafe_allow_html=True)
            
            with cols[1]:
                content = st.text_area(
                    "",
                    placeholder="O que você está fazendo pelo planeta hoje?",
                    height=80,
                    key="new_post_content",
                    label_visibility="collapsed"
                )
            
            # Ações
            action_cols = st.columns([2, 2, 2, 6])
            
            with action_cols[0]:
                st.button("📷 Foto", use_container_width=True, key="add_photo")
            with action_cols[1]:
                st.button("📍 Local", use_container_width=True, key="add_location")
            with action_cols[2]:
                st.button("🏷️ Tags", use_container_width=True, key="add_tags")
            with action_cols[3]:
                if st.button("🚀 **Publicar**", use_container_width=True, type="primary", key="publish"):
                    if content:
                        new_post = {
                            'id': f'post_{random.randint(10000, 99999)}',
                            'author': st.session_state.user_data['name'],
                            'author_username': st.session_state.user_data['username'],
                            'author_avatar': st.session_state.user_data['avatar'],
                            'author_level': st.session_state.user_data['level'],
                            'author_verified': st.session_state.user_data.get('verified', False),
                            'timestamp': datetime.now(),
                            'content': content,
                            'image': None,
                            'likes': 0,
                            'comments': [],
                            'shares': 0,
                            'user_liked': False,
                            'user_saved': False,
                            'tags': []
                        }
                        st.session_state.db_posts.insert(0, new_post)
                        st.success("✅ Publicado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("⚠️ Escreva algo antes de publicar!")
    
    @staticmethod
    def render_post(post):
        """Renderiza post com design moderno"""
        with st.container():
            st.markdown('<div class="post-card">', unsafe_allow_html=True)
            
            # Header do post
            header_cols = st.columns([1, 9, 1])
            
            with header_cols[0]:
                st.markdown(f"""
                <div class="post-author-avatar">{post['author_avatar']}</div>
                """, unsafe_allow_html=True)
            
            with header_cols[1]:
                verified = "✅" if post.get('author_verified') else ""
                st.markdown(f"""
                <div class="post-author-info">
                    <div class="post-author-name">
                        {post['author']} {verified}
                    </div>
                    <div class="post-author-meta">
                        @{post['author_username']} • {UIComponents.format_time(post['timestamp'])} • Nível {post['author_level']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with header_cols[2]:
                st.button("⋮", key=f"opt_{post['id']}", use_container_width=True)
            
            # Conteúdo
            st.markdown(f"""
            <div class="post-content">{post['content']}</div>
            """, unsafe_allow_html=True)
            
            # Tags
            if post.get('tags'):
                tags_html = " ".join([f'<span style="color: #3498db; margin-right: 8px;">{tag}</span>' for tag in post['tags']])
                st.markdown(f"""
                <div style="padding: 0 24px 16px; font-size: 14px;">{tags_html}</div>
                """, unsafe_allow_html=True)
            
            # Imagem placeholder
            if post.get('image'):
                st.markdown("""
                <div class="post-image-placeholder">🖼️</div>
                """, unsafe_allow_html=True)
            
            # Estatísticas
            st.markdown(f"""
            <div class="post-stats">
                <div class="post-stat">❤️ {post['likes']} curtidas</div>
                <div class="post-stat">💬 {len(post['comments'])} comentários</div>
                <div class="post-stat">🔄 {post['shares']} compartilhamentos</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ações
            action_cols = st.columns(4)
            
            with action_cols[0]:
                liked = post.get('user_liked', False)
                like_label = "❤️ Curtido" if liked else "🤍 Curtir"
                if st.button(like_label, key=f"like_{post['id']}", use_container_width=True):
                    idx = next(i for i, p in enumerate(st.session_state.db_posts) if p['id'] == post['id'])
                    st.session_state.db_posts[idx]['user_liked'] = not liked
                    st.session_state.db_posts[idx]['likes'] += 1 if not liked else -1
                    st.rerun()
            
            with action_cols[1]:
                if st.button("💬 Comentar", key=f"comm_{post['id']}", use_container_width=True):
                    st.session_state[f"show_comments_{post['id']}"] = not st.session_state.get(f"show_comments_{post['id']}", False)
                    st.rerun()
            
            with action_cols[2]:
                if st.button("🔄 Compartilhar", key=f"share_{post['id']}", use_container_width=True):
                    st.toast("🔄 Compartilhado!")
            
            with action_cols[3]:
                saved = post.get('user_saved', False)
                save_label = "⭐ Salvo" if saved else "☆ Salvar"
                if st.button(save_label, key=f"save_{post['id']}", use_container_width=True):
                    idx = next(i for i, p in enumerate(st.session_state.db_posts) if p['id'] == post['id'])
                    st.session_state.db_posts[idx]['user_saved'] = not saved
                    st.rerun()
            
            # Comentários
            if st.session_state.get(f"show_comments_{post['id']}", False):
                st.markdown("---")
                
                for comment in post['comments']:
                    comment_cols = st.columns([1, 11])
                    with comment_cols[0]:
                        st.markdown(comment.get('avatar', '👤'))
                    with comment_cols[1]:
                        st.markdown(f"**{comment['author']}**: {comment['text']}")
                        st.caption(UIComponents.format_time(comment['timestamp']))
                
                # Novo comentário
                new_comm_cols = st.columns([10, 2])
                with new_comm_cols[0]:
                    new_comment = st.text_input("", placeholder="Escreva um comentário...", 
                                               key=f"nc_{post['id']}", label_visibility="collapsed")
                with new_comm_cols[1]:
                    if st.button("Enviar", key=f"send_{post['id']}", use_container_width=True, type="primary"):
                        if new_comment:
                            idx = next(i for i, p in enumerate(st.session_state.db_posts) if p['id'] == post['id'])
                            st.session_state.db_posts[idx]['comments'].append({
                                'author': st.session_state.user_data['name'],
                                'avatar': st.session_state.user_data['avatar'],
                                'text': new_comment,
                                'timestamp': datetime.now()
                            })
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_trending():
        """Widget de trending topics moderno"""
        st.markdown('<div class="widget-title">🔥 Trending Topics</div>', unsafe_allow_html=True)
        
        for trend in st.session_state.db_trending:
            trend_icon = "📈" if trend['trend'] == 'up' else "📉" if trend['trend'] == 'down' else "➡️"
            
            st.markdown(f"""
            <div style='display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #f8f9fa; 
                        cursor: pointer; transition: all 0.2s;'
                 onmouseover="this.style.background='#f8f9fa'; this.style.marginLeft='8px';"
                 onmouseout="this.style.background='transparent'; this.style.marginLeft='0';">
                <span style='font-size: 18px; font-weight: 700; color: #7f8c8d; width: 30px;'>{trend['rank']}</span>
                <div style='flex: 1;'>
                    <div style='font-weight: 600; color: #2c3e50; font-size: 14px;'>{trend['tag']}</div>
                    <div style='font-size: 12px; color: #7f8c8d;'>{trend['posts']} posts</div>
                </div>
                <span style='font-size: 16px;'>{trend_icon}</span>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_suggestions():
        """Widget de sugestões moderno"""
        st.markdown('<div class="widget-title">👥 Quem Seguir</div>', unsafe_allow_html=True)
        
        for sugg in st.session_state.db_suggestions:
            cols = st.columns([2, 7, 3])
            
            with cols[0]:
                st.markdown(f"""
                <div style='font-size: 36px; text-align: center;'>{sugg['avatar']}</div>
                """, unsafe_allow_html=True)
            
            with cols[1]:
                verified = "✅" if sugg.get('verified') else ""
                st.markdown(f"""
                <div>
                    <div style='font-weight: 600; color: #2c3e50; font-size: 14px;'>
                        {sugg['name']} {verified}
                    </div>
                    <div style='font-size: 12px; color: #7f8c8d;'>@{sugg['username']}</div>
                    <div style='font-size: 12px; color: #7f8c8d; margin-top: 4px;'>{sugg['bio']}</div>
                    <div style='font-size: 11px; color: #3498db; margin-top: 4px;'>
                        {sugg['followers']:,} seguidores
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[2]:
                if st.button("Seguir", key=f"follow_{sugg['username']}", use_container_width=True):
                    st.toast(f"✅ Seguindo {sugg['name']}")
    
    @staticmethod
    def format_time(timestamp):
        """Formata tempo relativo"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 7:
            return timestamp.strftime("%d/%m/%Y")
        elif diff.days > 0:
            return f"{diff.days}d"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}min"
        else:
            return "agora"

# ========== TELA DE LOGIN ESTILIZADA (importada de login.py) ==========
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

USERS = {
    "estudante": {
        "password": "estudante123",
        "role": "Estudante",
        "full_name": "João Silva"
    },
    "gestor": {
        "password": "gestor123",
        "role": "Gestor",
        "full_name": "Maria Santos"
    },
    "nicolasfranca": {
        "password": "demo123",
        "role": "Administrador",
        "full_name": "Nicolas França"
    }
}

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.full_name = None
    st.session_state.user_data = None

def authenticate(username, password):
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = USERS[username]["role"]
        st.session_state.full_name = USERS[username]["full_name"]
        # Inicializa user_data para uso nos widgets de perfil
        if 'db_users' in st.session_state and username in st.session_state.db_users:
            st.session_state.user_data = st.session_state.db_users[username]
        else:
            # fallback mínimo se não houver db_users
            st.session_state.user_data = {
                'name': st.session_state.full_name or username,
                'username': username,
                'avatar': '👤',
                'level': 1,
                'followers': 0,
                'following': 0,
                'posts_count': 0,
                'bio': ''
            }
        return True
    return False

# CSS e layout do login
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { position: relative; min-height: 100vh; z-index: 0; }
    .stApp::before {
        content: "";
        position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -1;
        background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1000 1000\"><defs><linearGradient id=\"bg\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"100%\"><stop offset=\"0%\" style=\"stop-color:%234CAF50;stop-opacity:1\" /><stop offset=\"25%\" style=\"stop-color:%2366BB6A;stop-opacity:0.8\" /><stop offset=\"50%\" style=\"stop-color:%2381C784;stop-opacity:0.6\" /><stop offset=\"75%\" style=\"stop-color:%23A5D6A7;stop-opacity:0.4\" /><stop offset=\"100%\" style=\"stop-color:%23C8E6C9;stop-opacity:0.2\" /></linearGradient></defs><rect width=\"100%\" height=\"100%\" fill=\"url(%23bg)\"/><circle cx=\"200\" cy=\"200\" r=\"50\" fill=\"%23388E3C\" opacity=\"0.1\"><animate attributeName=\"r\" values=\"50;80;50\" dur=\"4s\" repeatCount=\"indefinite\"/></circle><circle cx=\"800\" cy=\"300\" r=\"60\" fill=\"%234CAF50\" opacity=\"0.15\"><animate attributeName=\"r\" values=\"60;90;60\" dur=\"5s\" repeatCount=\"indefinite\"/></circle><circle cx=\"400\" cy=\"700\" r=\"40\" fill=\"%2366BB6A\" opacity=\"0.1\"><animate attributeName=\"r\" values=\"40;70;40\" dur=\"3s\" repeatCount=\"indefinite\"/></circle><circle cx=\"700\" cy=\"800\" r=\"55\" fill=\"%23388E3C\" opacity=\"0.12\"><animate attributeName=\"r\" values=\"55;85;55\" dur=\"4.5s\" repeatCount=\"indefinite\"/></circle></svg>') no-repeat center center fixed;
        background-size: cover; width: 100vw; height: 100vh; opacity: 1;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(15px);
        padding: 3rem; border-radius: 25px; box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        text-align: center; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.3);
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
    .title { color: #2d5a27; font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    .subtitle { color: #5a7c76; font-size: 1.1rem; margin-bottom: 2rem; font-weight: 300; }
    .stButton > button { width: 100%; border-radius: 15px; height: 3.5rem; font-size: 1.2rem; font-weight: 600; background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); border: none; color: white; transition: all 0.4s ease; margin-top: 1.5rem; }
    .stButton > button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 12px 30px rgba(76, 175, 80, 0.4); }
    .success-msg { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: #155724; padding: 1rem; border-radius: 12px; margin: 1rem 0; text-align: center; font-weight: 500; }
    .error-msg { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); color: #721c24; padding: 1rem; border-radius: 12px; margin: 1rem 0; text-align: center; font-weight: 500; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    logo_base64 = get_base64_image("fotos/logotipo.png")
    if logo_base64:
        st.markdown(f'<img src="data:image/png;base64,{logo_base64}" width="64" class="logo-img">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">🌱 Ecoins</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema de Gestão Ambiental</p>', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
        password = st.text_input("🔒 Senha:", type="password", placeholder="Digite sua senha")
        if st.form_submit_button("🚀 Entrar", use_container_width=True):
            if username and password:
                with st.spinner("Verificando credenciais..."):
                    time.sleep(1)
                if authenticate(username, password):
                    st.markdown("""
                    <div class="success-msg">
                        ✅ Login realizado com sucesso! Bem-vindo!
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    time.sleep(1.2)
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="error-msg">
                        ❌ Usuário ou senha incorretos. Tente novamente.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-msg">
                    ⚠️ Por favor, preencha todos os campos.
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("🔧 Credenciais de Teste"):
        st.info("""
        **Estudante:**
        - Usuário: `estudante`
        - Senha: `estudante123`
        
        **Gestor:**
        - Usuário: `gestor`
        - Senha: `gestor123`
        """)
    st.stop()

# ========================= PÁGINAS =========================
def feed_page():
    """Página do feed principal com layout otimizado"""
    
    # Layout em 3 colunas com proporções ajustadas
    col_left, col_center, col_right = st.columns([1.2, 2.3, 1])
    
    # Coluna Esquerda
    with col_left:
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_profile_widget()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_challenges_widget()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Coluna Central
    with col_center:
        # Stories
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_stories()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Criar post
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_create_post()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Feed
        st.markdown('<div class="section-title">📰 Feed de Publicações</div>', unsafe_allow_html=True)
        
        for post in st.session_state.db_posts:
            UIComponents.render_post(post)
    
    # Coluna Direita
    with col_right:
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_trending()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            UIComponents.render_suggestions()
            st.markdown('</div>', unsafe_allow_html=True)



def other_pages():
    """Páginas em desenvolvimento"""
    page = st.session_state.get('current_page', 'feed')
    
    pages_info = {
        'education': ("📚", "Educação", "Aprenda sobre sustentabilidade e ganhe XP"),
        'challenges': ("🏆", "Desafios", "Complete missões e ganhe recompensas"),
        'marketplace': ("🛍️", "Marketplace", "Troque seus pontos por produtos sustentáveis"),
        'collection': ("📍", "Pontos de Coleta", "Encontre locais de reciclagem próximos"),
        'profile': ("👤", "Perfil", "Gerencie sua conta e veja suas conquistas")
    }
    
    if page in pages_info:
        icon, title, desc = pages_info[page]
        
        st.markdown(f"""
        <div style='text-align: center; padding: 60px 40px; 
                    background: linear-gradient(135deg, #27ae60, #3498db); 
                    border-radius: 24px; color: white; margin-bottom: 40px;'>
            <div style='font-size: 64px; margin-bottom: 16px;'>{icon}</div>
            <h2 style='margin-bottom: 8px;'>{title}</h2>
            <p style='opacity: 0.9;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🚧 Esta página está em desenvolvimento e estará disponível em breve!")
        
        if st.button("← Voltar ao Feed", type="primary"):
            st.session_state.current_page = 'feed'
            st.rerun()

# ========================= APLICAÇÃO PRINCIPAL =========================
def main_app():
    """Aplicação principal com navbar moderno"""
    UIComponents.render_modern_navbar()
    
    # Adicionar espaço após o navbar
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    page = st.session_state.get('current_page', 'feed')
    
    if page == 'feed':
        feed_page()
    else:
        other_pages()

# ========================= MAIN =========================
def main():
    """Função principal"""
    Database.init_database()
    load_ultra_modern_css()
    
    # O login_page antigo foi removido. O login estilizado já está acima.
    if not st.session_state.authenticated:
        # A tela de login estilizada já faz o st.stop(), então nada mais é necessário aqui.
        pass
    else:
        main_app()

if __name__ == "__main__":
    main()
