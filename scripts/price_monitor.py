#!/usr/bin/env python3
"""
Monitor de Preços — Planejamento Apartamento

Este script monitora preços dos itens do projeto em lojas online
e envia alertas quando o preço cai abaixo do valor desejado.

Uso:
  1. Preencha a lista ITEMS_TO_TRACK com os produtos
  2. Configure seu email para alertas (opcional)
  3. Execute: python3 scripts/price_monitor.py
  4. Para rodar automaticamente, configure um cron job

Dependências:
  pip install requests beautifulsoup4
"""

import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Instale as dependências: pip install requests beautifulsoup4")
    exit(1)


ROOT = Path(__file__).resolve().parents[1]
PRICES_FILE = ROOT / "data" / "prices_history.json"
ALERTS_FILE = ROOT / "data" / "price_alerts.json"


@dataclass
class Product:
    name: str
    category: str
    target_price: float  # Preço alvo para alerta
    keywords: str  # Palavras-chave para busca


# ============================================================
# 📋 CONFIGURE AQUI OS ITENS QUE VOCÊ QUER MONITORAR
# ============================================================

ITEMS_TO_TRACK = [
    # Ar-condicionado
    Product("Ar Split Samsung 9000 BTU Inverter", "AC", 1400.00, "ar condicionado split samsung 9000 btu inverter"),
    Product("Ar Split LG Dual Inverter 9000 BTU", "AC", 1500.00, "ar condicionado split lg dual inverter 9000"),
    Product("Ar Split Midea 9000 BTU", "AC", 1200.00, "ar condicionado split midea 9000 btu"),
    
    # Eletrodomésticos
    Product("Cooktop 4 Bocas Vidro Preto", "Cozinha", 400.00, "cooktop 4 bocas vidro preto"),
    Product("Forno Elétrico Embutir", "Cozinha", 800.00, "forno elétrico embutir 44 litros"),
    Product("Depurador de Ar 60cm", "Cozinha", 250.00, "depurador ar 60cm branco"),
    
    # Iluminação
    Product("Spot LED Embutir 7W 3000K", "Iluminação", 20.00, "spot led embutir 7w 3000k"),
    Product("Fita LED 5m 3000K", "Iluminação", 40.00, "fita led 5m 3000k branco quente"),
    
    # Banheiro
    Product("Torneira Banheiro Preta Fosca", "Banheiro", 150.00, "torneira banheiro preta fosca monocomando"),
    Product("Vaso Sanitário Suspenso", "Banheiro", 500.00, "vaso sanitário suspenso com caixa acoplada"),
    
    # Móveis
    Product("Painel TV MDF 160cm", "Sala", 600.00, "painel tv mdf 160cm madeira"),
    Product("Guarda-Roupa 2 Portas Espelho", "Quarto", 1800.00, "guarda roupa 2 portas espelho deslizante"),
    
    # ========================================
    # 🏠 AUTOMAÇÃO RESIDENCIAL (SMART HOME)
    # ========================================
    
    # Assistentes de Voz
    Product("Amazon Echo Dot 5", "Smart Home", 300.00, "echo dot 5 geração alexa"),
    Product("Amazon Echo Show 5", "Smart Home", 450.00, "echo show 5 alexa tela"),
    Product("Google Nest Mini", "Smart Home", 250.00, "google nest mini"),
    
    # Iluminação Smart
    Product("Lâmpada Smart Positivo WiFi", "Smart Home", 40.00, "lampada smart positivo wifi"),
    Product("Lâmpada Smart RGB Positivo", "Smart Home", 60.00, "lampada smart rgb positivo"),
    Product("Interruptor Smart Positivo 2 teclas", "Smart Home", 100.00, "interruptor smart positivo 2 teclas wifi"),
    Product("Interruptor Smart Sonoff Touch", "Smart Home", 80.00, "interruptor sonoff touch wifi"),
    
    # Controle IR (AC/TV)
    Product("Broadlink RM4 Mini", "Smart Home", 130.00, "broadlink rm4 mini controle universal"),
    Product("Positivo Smart Controle IR", "Smart Home", 90.00, "positivo smart controle ir universal"),
    Product("Moes IR Blaster Tuya", "Smart Home", 60.00, "moes ir blaster wifi tuya"),
    
    # Tomadas Smart
    Product("Tomada Smart Positivo", "Smart Home", 60.00, "tomada smart positivo wifi"),
    Product("Tomada Smart TP-Link Kasa", "Smart Home", 80.00, "tomada smart tp-link kasa"),
    
    # Fechadura Digital
    Product("Fechadura Digital Intelbras FR 220", "Smart Home", 800.00, "fechadura digital intelbras fr 220"),
    Product("Fechadura Digital Yale", "Smart Home", 1000.00, "fechadura digital yale"),
    
    # Câmeras
    Product("Câmera Tapo C200 TP-Link", "Smart Home", 150.00, "camera tapo c200 tp-link wifi"),
    Product("Câmera Intelbras iM3", "Smart Home", 180.00, "camera intelbras im3 wifi"),
    Product("Câmera Positivo Smart 360", "Smart Home", 200.00, "camera positivo smart 360"),
    
    # Sensores
    Product("Sensor Porta Zigbee", "Smart Home", 40.00, "sensor porta janela zigbee"),
    Product("Sensor Movimento Smart", "Smart Home", 50.00, "sensor movimento smart wifi"),
]


# ============================================================
# FUNÇÕES DE BUSCA DE PREÇOS
# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def search_zoom(keywords: str) -> list[dict]:
    """Busca preços no Zoom.com.br"""
    results = []
    try:
        url = f"https://www.zoom.com.br/search?q={quote_plus(keywords)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Encontrar cards de produto
        cards = soup.select("[data-testid='product-card']")[:5]
        for card in cards:
            try:
                title_el = card.select_one("[data-testid='product-card-name']")
                price_el = card.select_one("[data-testid='product-card-price']")
                
                if title_el and price_el:
                    title = title_el.get_text(strip=True)
                    price_text = price_el.get_text(strip=True)
                    price = parse_price(price_text)
                    if price:
                        results.append({
                            "title": title[:80],
                            "price": price,
                            "source": "Zoom",
                            "url": url
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"  [Zoom] Erro: {e}")
    
    return results


def search_buscape(keywords: str) -> list[dict]:
    """Busca preços no Buscapé"""
    results = []
    try:
        url = f"https://www.buscape.com.br/search?q={quote_plus(keywords)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Estrutura pode variar
        cards = soup.select(".ProductCard")[:5]
        for card in cards:
            try:
                title_el = card.select_one(".ProductCard_Name")
                price_el = card.select_one(".ProductCard_Price")
                
                if title_el and price_el:
                    title = title_el.get_text(strip=True)
                    price = parse_price(price_el.get_text(strip=True))
                    if price:
                        results.append({
                            "title": title[:80],
                            "price": price,
                            "source": "Buscapé",
                            "url": url
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"  [Buscapé] Erro: {e}")
    
    return results


def search_mercadolivre(keywords: str) -> list[dict]:
    """Busca preços no Mercado Livre"""
    results = []
    try:
        url = f"https://lista.mercadolivre.com.br/{quote_plus(keywords)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        items = soup.select(".ui-search-layout__item")[:5]
        for item in items:
            try:
                title_el = item.select_one(".ui-search-item__title")
                price_int = item.select_one(".andes-money-amount__fraction")
                
                if title_el and price_int:
                    title = title_el.get_text(strip=True)
                    price_cents = item.select_one(".andes-money-amount__cents")
                    
                    price_str = price_int.get_text(strip=True).replace(".", "")
                    if price_cents:
                        price_str += "." + price_cents.get_text(strip=True)
                    
                    price = float(price_str)
                    results.append({
                        "title": title[:80],
                        "price": price,
                        "source": "Mercado Livre",
                        "url": url
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"  [ML] Erro: {e}")
    
    return results


def parse_price(text: str) -> Optional[float]:
    """Extrai valor numérico de texto de preço"""
    if not text:
        return None
    # Remove R$, pontos de milhar, substitui vírgula por ponto
    clean = re.sub(r"[^\d,.]", "", text)
    clean = clean.replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return None


def search_all(product: Product) -> list[dict]:
    """Busca preço em todas as fontes"""
    results = []
    
    # Busca em cada fonte
    results.extend(search_mercadolivre(product.keywords))
    time.sleep(1)  # Evitar bloqueio
    
    results.extend(search_zoom(product.keywords))
    time.sleep(1)
    
    # Ordena por preço
    results.sort(key=lambda x: x["price"])
    
    return results


# ============================================================
# FUNÇÕES DE HISTÓRICO E ALERTAS
# ============================================================

def load_history() -> dict:
    """Carrega histórico de preços"""
    if PRICES_FILE.exists():
        return json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    return {}


def save_history(history: dict):
    """Salva histórico de preços"""
    PRICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PRICES_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def check_alerts(product: Product, results: list[dict]) -> list[dict]:
    """Verifica se algum preço está abaixo do alvo"""
    alerts = []
    for r in results:
        if r["price"] <= product.target_price:
            alerts.append({
                "product": product.name,
                "target": product.target_price,
                "found_price": r["price"],
                "title": r["title"],
                "source": r["source"],
                "savings": product.target_price - r["price"],
                "timestamp": datetime.now().isoformat()
            })
    return alerts


def print_alert(alert: dict):
    """Imprime alerta formatado"""
    print("\n" + "=" * 60)
    print(f"🔔 ALERTA DE PREÇO BAIXO!")
    print("=" * 60)
    print(f"Produto: {alert['product']}")
    print(f"Preço alvo: R$ {alert['target']:.2f}")
    print(f"Preço encontrado: R$ {alert['found_price']:.2f}")
    print(f"Economia: R$ {alert['savings']:.2f}")
    print(f"Título: {alert['title']}")
    print(f"Fonte: {alert['source']}")
    print("=" * 60)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("📊 MONITOR DE PREÇOS — PLANEJAMENTO APARTAMENTO")
    print(f"   Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    history = load_history()
    all_alerts = []
    
    for product in ITEMS_TO_TRACK:
        print(f"\n🔍 Buscando: {product.name}")
        print(f"   Preço alvo: R$ {product.target_price:.2f}")
        
        results = search_all(product)
        
        if results:
            best = results[0]
            print(f"   ✅ Melhor preço: R$ {best['price']:.2f} ({best['source']})")
            
            # Salva no histórico
            key = product.name
            if key not in history:
                history[key] = []
            history[key].append({
                "date": datetime.now().isoformat(),
                "price": best["price"],
                "source": best["source"]
            })
            
            # Verifica alertas
            alerts = check_alerts(product, results)
            if alerts:
                for alert in alerts:
                    print_alert(alert)
                all_alerts.extend(alerts)
        else:
            print(f"   ⚠️ Nenhum resultado encontrado")
        
        time.sleep(2)  # Pausa entre buscas
    
    # Salva histórico
    save_history(history)
    print(f"\n💾 Histórico salvo em: {PRICES_FILE}")
    
    # Salva alertas se houver
    if all_alerts:
        ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        existing_alerts = []
        if ALERTS_FILE.exists():
            existing_alerts = json.loads(ALERTS_FILE.read_text(encoding="utf-8"))
        existing_alerts.extend(all_alerts)
        ALERTS_FILE.write_text(
            json.dumps(existing_alerts, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"🔔 {len(all_alerts)} alerta(s) salvo(s) em: {ALERTS_FILE}")
    
    print("\n✅ Monitoramento concluído!")
    print("   Dica: Execute novamente amanhã ou configure um cron job")
    print("   Exemplo cron (todo dia às 9h): 0 9 * * * python3 /caminho/scripts/price_monitor.py")
    
    return 0


if __name__ == "__main__":
    exit(main())
