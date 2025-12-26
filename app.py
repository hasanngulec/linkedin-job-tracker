"""
📊 İş Başvurusu Takip ve Analiz Platformu
=========================================
n8n otomasyonundan gelen LinkedIn başvuru verilerini analiz eder.
Herhangi bir meslek alanı için kullanılabilir.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="İş Başvurusu Analiz Platformu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Tema uyumlu stil (açık ve karanlık tema desteği)
st.markdown("""
<style>
    /* Sosyal medya ikonları */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .social-links a img {
        transition: transform 0.2s;
    }
    
    .social-links a img:hover {
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)


def load_data(uploaded_file):
    """CSV dosyasını yükle ve işle"""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Tarih sütununu datetime'a çevir
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df = df.sort_values('Date', ascending=False)
        
        return df
    except Exception as e:
        st.error(f"Dosya yüklenirken hata: {e}")
        return None


def calculate_metrics(df):
    """Ana metrikleri hesapla"""
    total = len(df)
    
    # Status bazlı sayılar
    applied = len(df[df['Status'] == 'Applied']) if 'Status' in df.columns else 0
    rejected = len(df[df['Status'] == 'Rejected']) if 'Status' in df.columns else 0
    under_review = len(df[df['Status'] == 'Under Review']) if 'Status' in df.columns else 0
    interview = len(df[df['Status'] == 'Interview']) if 'Status' in df.columns else 0
    
    # Oranlar
    rejection_rate = (rejected / total * 100) if total > 0 else 0
    response_rate = ((rejected + interview + under_review) / total * 100) if total > 0 else 0
    interview_rate = (interview / total * 100) if total > 0 else 0
    
    # Benzersiz şirket sayısı
    unique_companies = df['Company'].nunique() if 'Company' in df.columns else 0
    
    return {
        'total': total,
        'applied': applied,
        'rejected': rejected,
        'under_review': under_review,
        'interview': interview,
        'rejection_rate': rejection_rate,
        'response_rate': response_rate,
        'interview_rate': interview_rate,
        'unique_companies': unique_companies
    }


def create_status_chart(df):
    """Durum dağılımı pasta grafiği"""
    if 'Status' not in df.columns:
        return None
    
    status_counts = df['Status'].value_counts()
    
    colors = {
        'Applied': '#00d4ff',
        'Rejected': '#ef4444',
        'Under Review': '#f97316',
        'Interview': '#22c55e'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.6,
        marker_colors=[colors.get(s, '#9e9e9e') for s in status_counts.index],
        textinfo='label+percent',
        textfont=dict(size=12, family='Outfit'),
        hovertemplate='<b>%{label}</b><br>Sayı: %{value}<br>Oran: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text='Başvuru Durumu Dağılımı', font=dict(size=18, color=None)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=60, b=80, l=20, r=20),
        annotations=[dict(
            text=f'<b>{len(df)}</b><br>Toplam',
            x=0.5, y=0.5,
            font=dict(size=20, color=None),
            showarrow=False
        )]
    )
    
    return fig


def create_timeline_chart(df):
    """Zaman bazlı başvuru grafiği"""
    if 'Date' not in df.columns:
        return None
    
    daily_counts = df.groupby(df['Date'].dt.date).size().reset_index(name='count')
    daily_counts['Date'] = pd.to_datetime(daily_counts['Date'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_counts['Date'],
        y=daily_counts['count'],
        mode='lines+markers',
        name='Başvuru Sayısı',
        line=dict(color=None, width=2, shape='spline'),
        marker=dict(size=6, color=None),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)',
        hovertemplate='<b>%{x|%d %B %Y}</b><br>Başvuru: %{y}<extra></extra>'
    ))
    
    # 7 günlük hareketli ortalama
    if len(daily_counts) > 7:
        daily_counts['ma7'] = daily_counts['count'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=daily_counts['Date'],
            y=daily_counts['ma7'],
            mode='lines',
            name='7 Günlük Ortalama',
            line=dict(color='#9c27b0', width=2, dash='dash'),
            hovertemplate='<b>%{x|%d %B %Y}</b><br>7 Günlük Ort: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text='Günlük Başvuru Trendi', font=dict(size=18, color=None)),
        xaxis=dict(
            title='Tarih',
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(color=None)
        ),
        yaxis=dict(
            title='Başvuru Sayısı',
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(color=None)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(t=80, b=60, l=60, r=20),
        hovermode='x unified'
    )
    
    return fig


def create_company_chart(df, top_n=15):
    """En çok başvurulan şirketler"""
    if 'Company' not in df.columns:
        return None
    
    company_counts = df['Company'].value_counts().head(top_n)
    
    fig = go.Figure(data=[go.Bar(
        x=company_counts.values,
        y=company_counts.index,
        orientation='h',
        marker=dict(
            color=company_counts.values,
            colorscale=[[0, '#e3f2fd'], [0.5, '#64b5f6'], [1, '#1976d2']],
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ),
        text=company_counts.values,
        textposition='outside',
        textfont=dict(color=None),
        hovertemplate='<b>%{y}</b><br>Başvuru: %{x}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=f'En Çok Başvurulan {top_n} Şirket', font=dict(size=18, color=None)),
        xaxis=dict(
            title='Başvuru Sayısı',
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(color=None)
        ),
        yaxis=dict(
            tickfont=dict(color=None),
            categoryorder='total ascending'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        margin=dict(t=60, b=60, l=200, r=60),
        height=max(400, top_n * 35)
    )
    
    return fig


def create_position_wordcloud_chart(df):
    """Pozisyon bazlı analiz"""
    if 'Position' not in df.columns:
        return None
    
    position_counts = df['Position'].value_counts().head(12)
    
    fig = go.Figure(data=[go.Bar(
        x=position_counts.index,
        y=position_counts.values,
        marker=dict(
            color=position_counts.values,
            colorscale=[[0, '#c8e6c9'], [0.5, '#ffc107'], [1, '#f44336']],
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ),
        text=position_counts.values,
        textposition='outside',
        textfont=dict(color=None),
        hovertemplate='<b>%{x}</b><br>Başvuru: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text='En Çok Başvurulan Pozisyonlar', font=dict(size=18, color=None)),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10, color=None),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title='Başvuru Sayısı',
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(color=None)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        margin=dict(t=60, b=120, l=60, r=20),
        height=450
    )
    
    return fig


def create_period_histogram(df, period='weekly'):
    """Haftalık veya aylık başvuru aktivitesi histogramı"""
    if 'Date' not in df.columns:
        return None
    
    df_temp = df.copy()
    
    if period == 'weekly':
        # Haftalık histogram
        df_temp['Period'] = df_temp['Date'].dt.to_period('W').astype(str)
        title = 'Haftalık Başvuru Aktivitesi'
        xaxis_title = 'Hafta'
    else:  # monthly
        # Aylık histogram
        df_temp['Period'] = df_temp['Date'].dt.to_period('M').astype(str)
        title = 'Aylık Başvuru Aktivitesi'
        xaxis_title = 'Ay'
    
    # Her dönem için başvuru sayısını hesapla
    period_counts = df_temp.groupby('Period').size().reset_index(name='count')
    period_counts = period_counts.sort_values('Period')
    
    # Histogram oluştur
    fig = go.Figure(data=go.Bar(
        x=period_counts['Period'],
        y=period_counts['count'],
        marker=dict(
            color=period_counts['count'],
            colorscale=[[0, '#e3f2fd'], [0.25, '#64b5f6'], [0.5, '#2196f3'], [0.75, '#1976d2'], [1, '#1565c0']],
            line=dict(color='rgba(0,0,0,0.1)', width=1),
            showscale=True,
            colorbar=dict(title="Başvuru Sayısı")
        ),
        text=period_counts['count'],
        textposition='outside',
        textfont=dict(color=None, size=11),
        hovertemplate='<b>%{x}</b><br>Başvuru: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=None)),
        xaxis=dict(
            title=xaxis_title,
            tickangle=45,
            tickfont=dict(color=None, size=10),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title='Başvuru Sayısı',
            tickfont=dict(color=None),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        margin=dict(t=60, b=100, l=60, r=20),
        height=450
    )
    
    return fig


def create_response_funnel(metrics):
    """Yanıt oranları huni grafiği"""
    stages = ['Toplam Başvuru', 'Görüntülendi', 'Mülakat Daveti', 'Red']
    values = [
        metrics['total'],
        metrics['under_review'],
        metrics['interview'],
        metrics['rejected']
    ]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        textfont=dict(color=None),
        marker=dict(
            color=['#2196f3', '#ff9800', '#4caf50', '#f44336'],
            line=dict(color='rgba(255,255,255,0.2)', width=2)
        ),
        connector=dict(fillcolor='rgba(0,0,0,0.05)', line=dict(color='rgba(0,0,0,0.1)'))
    ))
    
    fig.update_layout(
        title=dict(text='Başvuru Yanıt Hunisi', font=dict(size=18, color=None)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        margin=dict(t=60, b=20, l=20, r=20),
        height=350
    )
    
    return fig


def create_status_by_company(df, top_n=10):
    """Şirket bazlı durum dağılımı"""
    if 'Company' not in df.columns or 'Status' not in df.columns:
        return None
    
    top_companies = df['Company'].value_counts().head(top_n).index
    df_top = df[df['Company'].isin(top_companies)]
    
    status_company = df_top.groupby(['Company', 'Status']).size().unstack(fill_value=0)
    
    colors = {
        'Applied': '#00d4ff',
        'Rejected': '#ef4444',
        'Under Review': '#f97316',
        'Interview': '#22c55e'
    }
    
    fig = go.Figure()
    
    for status in status_company.columns:
        fig.add_trace(go.Bar(
            name=status,
            x=status_company.index,
            y=status_company[status],
            marker_color=colors.get(status, '#9e9e9e'),
            hovertemplate=f'<b>%{{x}}</b><br>{status}: %{{y}}<extra></extra>'
        ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(text=f'Top {top_n} Şirket - Durum Dağılımı', font=dict(size=18, color=None)),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10, color=None),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title='Başvuru Sayısı',
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(color=None)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=None),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(t=80, b=120, l=60, r=20),
        height=500
    )
    
    return fig


def create_html_dashboard(df, metrics):
    """HTML dashboard oluştur"""
    # Grafikleri oluştur
    status_chart = create_status_chart(df)
    timeline_chart = create_timeline_chart(df)
    company_chart = create_company_chart(df, top_n=15)
    position_chart = create_position_wordcloud_chart(df)
    funnel_chart = create_response_funnel(metrics)
    status_by_company_chart = create_status_by_company(df, top_n=10)
    weekly_histogram = create_period_histogram(df, period='weekly')
    monthly_histogram = create_period_histogram(df, period='monthly')
    
    # Grafikleri HTML'e çevir (sadece ilk grafikte Plotly.js dahil)
    status_html = status_chart.to_html(include_plotlyjs='cdn', div_id='status_chart') if status_chart else ""
    timeline_html = timeline_chart.to_html(include_plotlyjs=False, div_id='timeline_chart') if timeline_chart else ""
    company_html = company_chart.to_html(include_plotlyjs=False, div_id='company_chart') if company_chart else ""
    position_html = position_chart.to_html(include_plotlyjs=False, div_id='position_chart') if position_chart else ""
    funnel_html = funnel_chart.to_html(include_plotlyjs=False, div_id='funnel_chart') if funnel_chart else ""
    status_by_company_html = status_by_company_chart.to_html(include_plotlyjs=False, div_id='status_by_company_chart') if status_by_company_chart else ""
    weekly_html = weekly_histogram.to_html(include_plotlyjs=False, div_id='weekly_chart') if weekly_histogram else ""
    monthly_html = monthly_histogram.to_html(include_plotlyjs=False, div_id='monthly_chart') if monthly_histogram else ""
    
    # Tablo HTML'i
    display_cols = ['Date', 'Company', 'Position', 'Status']
    if 'Gmail Link' in df.columns:
        display_cols.append('Gmail Link')
    available_cols = [c for c in display_cols if c in df.columns]
    df_display = df[available_cols].head(100)
    
    table_html = df_display.to_html(
        classes='table table-striped table-hover',
        table_id='applications_table',
        escape=False,
        index=False
    )
    
    # En çok başvurulan şirketler
    top_companies = df['Company'].value_counts().head(10) if 'Company' in df.columns else pd.Series()
    top_companies_html = ""
    if len(top_companies) > 0:
        top_companies_html = "<h3>🏢 En Çok Başvurulan 10 Şirket</h3><ul>"
        for idx, (company, count) in enumerate(top_companies.items(), 1):
            top_companies_html += f"<li><strong>{idx}. {company}</strong>: {count} başvuru</li>"
        top_companies_html += "</ul>"
    
    # Durum dağılımı
    status_dist = df['Status'].value_counts() if 'Status' in df.columns else pd.Series()
    status_dist_html = ""
    if len(status_dist) > 0:
        status_dist_html = "<h3>📊 Durum Dağılımı</h3><ul>"
        for status, count in status_dist.items():
            percentage = (count / len(df)) * 100 if len(df) > 0 else 0
            status_dist_html += f"<li><strong>{status}</strong>: {count} ({percentage:.1f}%)</li>"
        status_dist_html += "</ul>"
    
    # HTML template
    html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İş Başvurusu Analiz Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        .chart-container {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        
        .info-box h3 {{
            color: #1976d2;
            margin-bottom: 15px;
        }}
        
        .info-box ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .info-box li {{
            padding: 8px 0;
            border-bottom: 1px solid #bbdefb;
        }}
        
        .info-box li:last-child {{
            border-bottom: none;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
        }}
        
        table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        table tr:hover {{
            background: #f5f5f5;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 İş Başvurusu Analiz Dashboard</h1>
            <p>Rapor Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{metrics['total']}</div>
                <div class="metric-label">Toplam Başvuru</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['unique_companies']}</div>
                <div class="metric-label">Farklı Şirket</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['interview']}</div>
                <div class="metric-label">Mülakat Daveti</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['under_review']}</div>
                <div class="metric-label">İnceleniyor</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['rejection_rate']:.1f}%</div>
                <div class="metric-label">Red Oranı</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['response_rate']:.1f}%</div>
                <div class="metric-label">Yanıt Oranı</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Genel İstatistikler</h2>
            <div class="info-box">
                <h3>Detaylı Metrikler</h3>
                <ul>
                    <li><strong>Toplam Başvuru:</strong> {metrics['total']}</li>
                    <li><strong>Benzersiz Şirket Sayısı:</strong> {metrics['unique_companies']}</li>
                    <li><strong>Mülakat Daveti:</strong> {metrics['interview']}</li>
                    <li><strong>İnceleniyor:</strong> {metrics['under_review']}</li>
                    <li><strong>Reddedilen:</strong> {metrics['rejected']}</li>
                    <li><strong>Başvuru Yapılan:</strong> {metrics['applied']}</li>
                </ul>
            </div>
            <div class="info-box">
                <h3>Oranlar</h3>
                <ul>
                    <li><strong>Red Oranı:</strong> {metrics['rejection_rate']:.1f}%</li>
                    <li><strong>Yanıt Oranı:</strong> {metrics['response_rate']:.1f}%</li>
                    <li><strong>Mülakat Oranı:</strong> {metrics['interview_rate']:.1f}%</li>
                </ul>
            </div>
            {top_companies_html}
            {status_dist_html}
        </div>
        
        <div class="section">
            <h2>📊 Başvuru Durumu Dağılımı</h2>
            <div class="chart-container">
                {status_html}
            </div>
        </div>
        
        <div class="section">
            <h2>📅 Günlük Başvuru Trendi</h2>
            <div class="chart-container">
                {timeline_html}
            </div>
        </div>
        
        <div class="section">
            <h2>🏢 En Çok Başvurulan Şirketler</h2>
            <div class="chart-container">
                {company_html}
            </div>
        </div>
        
        <div class="section">
            <h2>💼 En Çok Başvurulan Pozisyonlar</h2>
            <div class="chart-container">
                {position_html}
            </div>
        </div>
        
        <div class="section">
            <h2>🔄 Başvuru Yanıt Hunisi</h2>
            <div class="chart-container">
                {funnel_html}
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Şirket Bazlı Durum Dağılımı</h2>
            <div class="chart-container">
                {status_by_company_html}
            </div>
        </div>
        
        <div class="section">
            <h2>📅 Haftalık Başvuru Aktivitesi</h2>
            <div class="chart-container">
                {weekly_html}
            </div>
        </div>
        
        <div class="section">
            <h2>📆 Aylık Başvuru Aktivitesi</h2>
            <div class="chart-container">
                {monthly_html}
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Başvuru Detayları (İlk 100 Kayıt)</h2>
            <div class="chart-container">
                {table_html}
            </div>
        </div>
        
        <div class="footer">
            <p><strong>📊 İş Başvurusu Analiz Platformu</strong></p>
            <p>n8n + Streamlit ile güçlendirilmiştir</p>
            <p>Rapor Oluşturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
    return html_content


def main():
    # Header - Streamlit'in kendi fonksiyonlarını kullan
    st.title("📊 İş Başvurusu Analiz Platformu")
    st.markdown("**n8n otomasyonundan gelen LinkedIn başvuru verilerinizi analiz edin**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        # Sosyal medya linkleri
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
            <a href="https://www.linkedin.com/in/hasan-tahsin-güleç-977955199" target="_blank" style="text-decoration: none;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="32" height="32" alt="LinkedIn">
            </a>
            <a href="https://github.com/hasanngulec" target="_blank" style="text-decoration: none;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="32" height="32" alt="GitHub">
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📁 Veri Yükleme")
        st.info("💡 **Bilgi:** n8n workflow'unuzdan dışa aktardığınız CSV dosyasını yükleyin.")
        
        uploaded_file = st.file_uploader(
            "CSV dosyası seçin",
            type=['csv'],
            help="n8n'den export ettiğiniz başvuru verilerini içeren CSV dosyası"
        )
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Ayarlar")
        
        # Demo veri seçeneği
        use_demo = st.checkbox("Demo veri kullan", value=False, help="Örnek veri ile platformu test edin")
        
        if uploaded_file or use_demo:
            st.markdown("---")
            st.markdown("### 🎯 Filtreler")
    
    # Ana içerik
    if uploaded_file is None and not use_demo:
        # Karşılama ekranı
        st.markdown("## 📤 Başlamak için veri yükleyin")
        st.markdown("Sol panelden n8n otomasyonunuzdan aldığınız CSV dosyasını yükleyin veya demo veriyi aktifleştirin.")
        st.markdown("---")
        
        st.markdown("### 🚀 Nasıl Kullanılır?")
        st.markdown("""
        1. **n8n Workflow'u çalıştırın** - LinkedIn email'leriniz işlenir
        2. **Google Sheets'ten CSV olarak dışa aktarın** veya doğrudan n8n'den export alın
        3. **CSV dosyasını buraya yükleyin**
        4. **Analizlerinizi görüntüleyin!**
        """)
        
        st.markdown("---")
        
        st.markdown("### 📊 Neler Analiz Edilir?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - 📈 **Başvuru Trendi** - Günlük/haftalık başvuru sayıları
            - 🏢 **Şirket Analizi** - En çok başvurulan şirketler
            - 💼 **Pozisyon Analizi** - Popüler pozisyonlar ve roller
            """)
        with col2:
            st.markdown("""
            - 📊 **Durum Dağılımı** - Kabul/Red/İnceleme oranları
            - 🎯 **Yanıt Oranları** - Şirket geri dönüş metrikleri
            - 📅 **Zaman Analizi** - Haftalık aktivite haritası
            """)
        
        return
    
    # Veri yükleme
    if use_demo:
        # sample_data.csv dosyasından demo veri yükle
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sample_data_path = os.path.join(script_dir, 'sample_data.csv')
        
        try:
            df = pd.read_csv(sample_data_path)
            # Tarih sütununu datetime'a çevir
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df = df.dropna(subset=['Date'])
                df = df.sort_values('Date', ascending=False)
            st.info("🎮 Demo verisi kullanılıyor (sample_data.csv). Gerçek verilerinizi yüklemek için sol panelden CSV dosyanızı seçin.")
        except FileNotFoundError:
            st.error("❌ sample_data.csv dosyası bulunamadı. Lütfen dosyanın proje klasöründe olduğundan emin olun.")
            return
    else:
        df = load_data(uploaded_file)
        if df is None:
            return
    
    # Sidebar filtreleri
    with st.sidebar:
        if 'Date' in df.columns:
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.date_input(
                "Tarih Aralığı",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if len(date_range) == 2:
                df = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
        
        if 'Status' in df.columns:
            statuses = st.multiselect(
                "Durum Filtresi",
                options=df['Status'].unique().tolist(),
                default=df['Status'].unique().tolist()
            )
            if statuses:
                df = df[df['Status'].isin(statuses)]
        
        if 'Company' in df.columns:
            # Tüm benzersiz şirketleri al
            all_companies = sorted(df['Company'].unique().tolist())
            
            # Session state ile seçilen şirketi takip et
            if 'selected_company_filter' not in st.session_state:
                st.session_state.selected_company_filter = None
            
            # Şirket seçimi - selectbox içinde yazarak arama yapılabilir
            # Dropdown'ı açıp yazdığınızda otomatik olarak filtreleme yapılır
            selected_company = st.selectbox(
                "🔍 Şirket Filtresi",
                options=[None] + all_companies,
                format_func=lambda x: "Tüm şirketler" if x is None else x,
                index=0 if st.session_state.selected_company_filter is None else (all_companies.index(st.session_state.selected_company_filter) + 1 if st.session_state.selected_company_filter in all_companies else 0),
                key="company_selectbox"
            )
            
            # Seçimi session state'e kaydet
            st.session_state.selected_company_filter = selected_company
            
            # Filtreleme uygula
            if selected_company:
                df = df[df['Company'] == selected_company]
            # None seçildiyse tüm şirketleri göster (filtreleme yapılmaz)
    
    # Metrikleri hesapla
    metrics = calculate_metrics(df)
    
    # Metrik kartları
    st.markdown("## 📈 Genel Bakış")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Toplam Başvuru", f"{metrics['total']}")
    
    with col2:
        st.metric("Farklı Şirket", f"{metrics['unique_companies']}")
    
    with col3:
        st.metric("Mülakat Daveti", f"{metrics['interview']}")
    
    with col4:
        st.metric("İnceleniyor", f"{metrics['under_review']}")
    
    with col5:
        st.metric("Red Oranı", f"{metrics['rejection_rate']:.1f}%")
    
    # Grafikler - Üst satır
    st.markdown("## 📊 Detaylı Analizler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_status_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_response_funnel(metrics)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Zaman serisi grafiği
    fig = create_timeline_chart(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Alt grafikler
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_company_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_position_wordcloud_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Histogram ve stacked bar
    col1, col2 = st.columns(2)
    
    with col1:
        # Haftalık/Aylık seçimi
        period_option = st.radio(
            "Görünüm:",
            options=['weekly', 'monthly'],
            format_func=lambda x: '📅 Haftalık' if x == 'weekly' else '📆 Aylık',
            horizontal=True,
            key="period_selector"
        )
        
        fig = create_period_histogram(df, period=period_option)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_status_by_company(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Veri tablosu
    st.markdown("## 📋 Başvuru Detayları")
    
    # Tablo için sütun seçimi
    display_cols = ['Date', 'Company', 'Position', 'Status']
    if 'Gmail Link' in df.columns:
        display_cols.append('Gmail Link')
    
    available_cols = [c for c in display_cols if c in df.columns]
    
    st.dataframe(
        df[available_cols].head(50),
        use_container_width=True,
        hide_index=True,
        column_config={
            'Date': st.column_config.DateColumn('Tarih', format='DD/MM/YYYY'),
            'Company': st.column_config.TextColumn('Şirket'),
            'Position': st.column_config.TextColumn('Pozisyon'),
            'Status': st.column_config.TextColumn('Durum'),
            'Gmail Link': st.column_config.LinkColumn('Gmail', display_text='📧 Aç')
        }
    )
    
    # Export seçeneği
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 CSV İndir",
            data=csv,
            file_name=f"basvuru_analiz_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # HTML Dashboard oluştur
        html_dashboard = create_html_dashboard(df, metrics)
        st.download_button(
            label="📊 Dashboard İndir (HTML)",
            data=html_dashboard,
            file_name=f"basvuru_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            help="Tüm grafikler ve analizlerle birlikte interaktif HTML dashboard"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("**📊 İş Başvurusu Analiz Platformu** | n8n + Streamlit ile güçlendirilmiştir")


if __name__ == "__main__":
    main()

