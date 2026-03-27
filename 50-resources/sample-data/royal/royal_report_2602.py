#!/usr/bin/env python3
"""Royal 2026년 2월 전 채널 종합 보고서 생성"""

import csv
from collections import defaultdict

# ── 1. B2B 발주 데이터 분석 ──
b2b_by_type = defaultdict(int)  # 거래처유형별 매출
b2b_by_customer = defaultdict(int)  # 거래처별 매출
bloei_orders = []  # BLOEI 비데 발주 추적
b2b_total = 0
cancelled_total = 0

with open('/Users/rhim/Projects/do-better-workspace/50-resources/sample-data/royal_orders_2602.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        amount = int(row['합계'])
        status = row['상태']
        customer_type = row['거래처유형']

        if '취소' in status:
            cancelled_total += amount
            continue

        b2b_total += amount
        b2b_by_type[customer_type] += amount
        b2b_by_customer[row['거래처명']] += amount

        if 'BLOEI' in row['상품명']:
            bloei_orders.append({
                'date': row['발주일'],
                'customer': row['거래처명'],
                'type': customer_type,
                'product': row['상품명'],
                'qty': int(row['수량']),
                'amount': amount,
                'status': status
            })

# ── 2. 온라인 판매 데이터 분석 ──
online_by_channel = defaultdict(int)
online_by_category = defaultdict(int)
online_by_week = defaultdict(int)
online_total = 0
online_cancelled = 0
online_orders_count = 0

with open('/Users/rhim/Projects/do-better-workspace/50-resources/sample-data/royal_online_sales_2602.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        amount = int(row['합계'])
        status = row['주문상태']

        if '취소' in status or '반품' in status:
            online_cancelled += amount
            continue

        online_total += amount
        online_by_channel[row['채널']] += amount
        online_by_category[row['카테고리']] += amount
        online_orders_count += 1

        # 주차별
        day = int(row['주문일'].split('-')[2])
        if day <= 7:
            online_by_week['1주차 (1-7일)'] += amount
        elif day <= 14:
            online_by_week['2주차 (8-14일)'] += amount
        elif day <= 21:
            online_by_week['3주차 (15-21일)'] += amount
        else:
            online_by_week['4주차 (22-28일)'] += amount

# ── 3. 재고 데이터 분석 ──
inventory_items = []
critical_items = []  # 재고일수 < 7일
warning_items = []   # 재고일수 < 14일

with open('/Users/rhim/Projects/do-better-workspace/50-resources/sample-data/royal_inventory_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['상품명'].strip():
            continue
        item = {
            'category': row['분류'],
            'name': row['상품명'],
            'code': row['코드'],
            'stock': int(row['총재고']),
            'daily_ship': float(row['일출하량']),
            'stock_days': float(row['재고일수']),
            'trend_w1': int(row['1주차출하']),
            'trend_w4': int(row['4주차출하']),
            'note': row['비고']
        }
        inventory_items.append(item)
        if item['stock_days'] < 7:
            critical_items.append(item)
        elif item['stock_days'] < 14:
            warning_items.append(item)

# ── 4. BLOEI 비데 발주 추이 (주차별) ──
bloei_by_week = defaultdict(lambda: {'qty': 0, 'amount': 0})
for order in bloei_orders:
    day = int(order['date'].split('-')[2])
    if day <= 7:
        week = '1주차'
    elif day <= 14:
        week = '2주차'
    elif day <= 21:
        week = '3주차'
    else:
        week = '4주차'
    bloei_by_week[week]['qty'] += order['qty']
    bloei_by_week[week]['amount'] += order['amount']

bloei_by_type = defaultdict(lambda: {'qty': 0, 'amount': 0})
for order in bloei_orders:
    bloei_by_type[order['type']]['qty'] += order['qty']
    bloei_by_type[order['type']]['amount'] += order['amount']

# ── 계산 ──
grand_total = b2b_total + online_total
b2b_pct = b2b_total / grand_total * 100
online_pct = online_total / grand_total * 100

# ── 숫자 포맷 ──
def fmt(n):
    if n >= 100000000:
        return f"{n/100000000:.1f}억"
    elif n >= 10000000:
        return f"{n/10000:.0f}만"
    elif n >= 10000:
        return f"{n/10000:.1f}만"
    else:
        return f"{n:,}"

def fmt_full(n):
    return f"{n:,}"

# ── HTML 보고서 생성 ──
html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Royal 2026년 2월 전 채널 종합 보고서</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Noto Sans KR', sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    padding: 40px 20px;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}

  /* Header */
  .header {{
    text-align: center;
    margin-bottom: 48px;
    padding: 40px;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 16px;
  }}
  .header h1 {{
    font-size: 32px; font-weight: 700; color: #f8fafc;
    margin-bottom: 8px;
  }}
  .header .subtitle {{
    font-size: 16px; color: #94a3b8; font-weight: 300;
  }}
  .header .date {{
    font-size: 14px; color: #64748b; margin-top: 12px;
  }}

  /* KPI Cards */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 40px;
  }}
  .kpi-card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  .kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }}
  .kpi-card:nth-child(1)::before {{ background: linear-gradient(90deg, #3b82f6, #60a5fa); }}
  .kpi-card:nth-child(2)::before {{ background: linear-gradient(90deg, #10b981, #34d399); }}
  .kpi-card:nth-child(3)::before {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}

  .kpi-label {{ font-size: 13px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
  .kpi-value {{ font-size: 36px; font-weight: 700; color: #f8fafc; }}
  .kpi-sub {{ font-size: 14px; color: #64748b; margin-top: 8px; }}

  /* Section */
  .section {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 24px;
  }}
  .section h2 {{
    font-size: 20px; font-weight: 600; color: #f8fafc;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #334155;
  }}
  .section h3 {{
    font-size: 16px; font-weight: 500; color: #cbd5e1;
    margin: 20px 0 12px;
  }}

  /* Charts */
  .chart-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    margin-bottom: 24px;
  }}
  .chart-box {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
  }}
  .chart-box h3 {{
    font-size: 15px; font-weight: 500; color: #cbd5e1;
    margin-bottom: 16px;
  }}
  .chart-wrapper {{
    position: relative;
    height: 280px;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }}
  th {{
    background: #0f172a;
    color: #94a3b8;
    font-weight: 500;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid #334155;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  td {{
    padding: 12px 16px;
    border-bottom: 1px solid #1e293b;
    color: #e2e8f0;
  }}
  tr:hover td {{ background: rgba(59, 130, 246, 0.05); }}
  .text-right {{ text-align: right; }}

  /* Status badges */
  .badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
  }}
  .badge-critical {{ background: #450a0a; color: #fca5a5; border: 1px solid #991b1b; }}
  .badge-warning {{ background: #451a03; color: #fcd34d; border: 1px solid #92400e; }}
  .badge-ok {{ background: #052e16; color: #86efac; border: 1px solid #166534; }}

  /* Insight cards */
  .insight-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 20px;
  }}
  .insight-card {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 24px;
  }}
  .insight-card .number {{
    font-size: 14px;
    font-weight: 600;
    color: #3b82f6;
    margin-bottom: 8px;
  }}
  .insight-card .title {{
    font-size: 15px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
  }}
  .insight-card .desc {{
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.6;
  }}

  /* Action items */
  .action-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 20px;
  }}
  .action-card {{
    background: #0f172a;
    border-radius: 10px;
    padding: 24px;
    border-left: 3px solid;
  }}
  .action-card:nth-child(1) {{ border-color: #3b82f6; }}
  .action-card:nth-child(2) {{ border-color: #10b981; }}
  .action-card:nth-child(3) {{ border-color: #f59e0b; }}
  .action-card .tag {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}
  .action-card:nth-child(1) .tag {{ color: #60a5fa; }}
  .action-card:nth-child(2) .tag {{ color: #34d399; }}
  .action-card:nth-child(3) .tag {{ color: #fbbf24; }}
  .action-card .title {{
    font-size: 15px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
  }}
  .action-card .desc {{
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.6;
  }}

  .full-width {{ grid-column: 1 / -1; }}

  @media (max-width: 768px) {{
    .kpi-grid, .chart-grid, .insight-grid, .action-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
  <h1>Royal 2026년 2월 전 채널 종합 보고서</h1>
  <div class="subtitle">B2B + Online 전 채널 매출 현황 및 재고 분석</div>
  <div class="date">보고 기간: 2026년 2월 1일 - 2월 28일 | 작성일: 2026-03-23</div>
</div>

<!-- KPI Cards -->
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">전 채널 합산 매출</div>
    <div class="kpi-value">{grand_total/100000000:.1f}억</div>
    <div class="kpi-sub">{fmt_full(grand_total)}원</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">B2B vs 온라인 비중</div>
    <div class="kpi-value">{b2b_pct:.0f}% : {online_pct:.0f}%</div>
    <div class="kpi-sub">B2B {fmt(b2b_total)}원 / 온라인 {fmt(online_total)}원</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">거래처 유형 TOP</div>
    <div class="kpi-value">시공사</div>
    <div class="kpi-sub">{fmt(b2b_by_type.get('시공사', 0))}원 ({b2b_by_type.get('시공사', 0)/b2b_total*100:.0f}%)</div>
  </div>
</div>

<!-- Charts Row 1 -->
<div class="chart-grid">
  <div class="chart-box">
    <h3>B2B vs 온라인 매출 비중</h3>
    <div class="chart-wrapper">
      <canvas id="channelPie"></canvas>
    </div>
  </div>
  <div class="chart-box">
    <h3>거래처 유형별 B2B 매출</h3>
    <div class="chart-wrapper">
      <canvas id="b2bTypeBar"></canvas>
    </div>
  </div>
</div>

<!-- Charts Row 2 -->
<div class="chart-grid">
  <div class="chart-box">
    <h3>온라인 채널별 매출</h3>
    <div class="chart-wrapper">
      <canvas id="onlineChannelBar"></canvas>
    </div>
  </div>
  <div class="chart-box">
    <h3>BLOEI 비데 주차별 발주량 추이</h3>
    <div class="chart-wrapper">
      <canvas id="bloeiTrend"></canvas>
    </div>
  </div>
</div>

<!-- BLOEI Detail -->
<div class="section">
  <h2>BLOEI 비데 발주 상세</h2>

  <h3>거래처 유형별 BLOEI 발주</h3>
  <table>
    <thead>
      <tr><th>거래처 유형</th><th class="text-right">수량</th><th class="text-right">금액</th><th class="text-right">비중</th></tr>
    </thead>
    <tbody>"""

bloei_total_amount = sum(v['amount'] for v in bloei_by_type.values())
bloei_total_qty = sum(v['qty'] for v in bloei_by_type.values())
for btype, data in sorted(bloei_by_type.items(), key=lambda x: x[1]['amount'], reverse=True):
    pct = data['amount'] / bloei_total_amount * 100
    html += f"""
      <tr>
        <td>{btype}</td>
        <td class="text-right">{data['qty']}개</td>
        <td class="text-right">{fmt_full(data['amount'])}원</td>
        <td class="text-right">{pct:.1f}%</td>
      </tr>"""

html += f"""
      <tr style="font-weight:600; border-top: 2px solid #334155;">
        <td>합계</td>
        <td class="text-right">{bloei_total_qty}개</td>
        <td class="text-right">{fmt_full(bloei_total_amount)}원</td>
        <td class="text-right">100%</td>
      </tr>
    </tbody>
  </table>

  <h3 style="margin-top:28px;">주차별 발주 추이</h3>
  <table>
    <thead>
      <tr><th>주차</th><th class="text-right">수량</th><th class="text-right">금액</th><th>추세</th></tr>
    </thead>
    <tbody>"""

for week in ['1주차', '2주차', '3주차', '4주차']:
    data = bloei_by_week[week]
    # trend arrow
    trend = ''
    if week != '1주차':
        prev_week = {'2주차': '1주차', '3주차': '2주차', '4주차': '3주차'}[week]
        prev = bloei_by_week[prev_week]['qty']
        if prev > 0:
            change = (data['qty'] - prev) / prev * 100
            if change > 0:
                trend = f'<span style="color:#34d399">+{change:.0f}%</span>'
            else:
                trend = f'<span style="color:#fca5a5">{change:.0f}%</span>'
    html += f"""
      <tr>
        <td>{week}</td>
        <td class="text-right">{data['qty']}개</td>
        <td class="text-right">{fmt_full(data['amount'])}원</td>
        <td>{trend}</td>
      </tr>"""

html += """
    </tbody>
  </table>
</div>

<!-- Inventory Risk -->
<div class="section">
  <h2>재고 위험 품목 현황</h2>

  <div class="chart-grid" style="margin-bottom:24px;">
    <div class="chart-box" style="grid-column: 1/-1;">
      <h3>품목별 재고일수 (위험 순서)</h3>
      <div style="position:relative; height:350px;">
        <canvas id="inventoryRisk"></canvas>
      </div>
    </div>
  </div>

  <h3>긴급 발주 필요 (재고일수 7일 미만)</h3>
  <table>
    <thead>
      <tr><th>분류</th><th>상품명</th><th>코드</th><th class="text-right">총재고</th><th class="text-right">일출하량</th><th class="text-right">재고일수</th><th>출하추이</th><th>상태</th></tr>
    </thead>
    <tbody>"""

for item in sorted(critical_items, key=lambda x: x['stock_days']):
    trend_change = ((item['trend_w4'] - item['trend_w1']) / item['trend_w1'] * 100) if item['trend_w1'] > 0 else 0
    trend_text = f'<span style="color:#fca5a5">W1:{item["trend_w1"]} -> W4:{item["trend_w4"]} (+{trend_change:.0f}%)</span>' if trend_change > 0 else f'W1:{item["trend_w1"]} -> W4:{item["trend_w4"]}'
    html += f"""
      <tr>
        <td>{item['category']}</td>
        <td>{item['name']}</td>
        <td><code style="color:#94a3b8">{item['code']}</code></td>
        <td class="text-right">{item['stock']}</td>
        <td class="text-right">{item['daily_ship']}</td>
        <td class="text-right"><span class="badge badge-critical">{item['stock_days']}일</span></td>
        <td>{trend_text}</td>
        <td><span class="badge badge-critical">{item['note'] or '위험'}</span></td>
      </tr>"""

html += """
    </tbody>
  </table>

  <h3 style="margin-top:24px;">주의 필요 (재고일수 7-14일)</h3>
  <table>
    <thead>
      <tr><th>분류</th><th>상품명</th><th>코드</th><th class="text-right">총재고</th><th class="text-right">일출하량</th><th class="text-right">재고일수</th><th>출하추이</th><th>상태</th></tr>
    </thead>
    <tbody>"""

for item in sorted(warning_items, key=lambda x: x['stock_days']):
    trend_change = ((item['trend_w4'] - item['trend_w1']) / item['trend_w1'] * 100) if item['trend_w1'] > 0 else 0
    trend_text = f'<span style="color:#fcd34d">W1:{item["trend_w1"]} -> W4:{item["trend_w4"]} (+{trend_change:.0f}%)</span>' if trend_change > 0 else f'W1:{item["trend_w1"]} -> W4:{item["trend_w4"]}'
    html += f"""
      <tr>
        <td>{item['category']}</td>
        <td>{item['name']}</td>
        <td><code style="color:#94a3b8">{item['code']}</code></td>
        <td class="text-right">{item['stock']}</td>
        <td class="text-right">{item['daily_ship']}</td>
        <td class="text-right"><span class="badge badge-warning">{item['stock_days']}일</span></td>
        <td>{trend_text}</td>
        <td><span class="badge badge-warning">{item['note'] or '주의'}</span></td>
      </tr>"""

html += """
    </tbody>
  </table>
</div>

<!-- B2B 거래처 상세 -->
<div class="section">
  <h2>B2B 거래처별 매출 TOP 10</h2>
  <table>
    <thead>
      <tr><th>#</th><th>거래처명</th><th class="text-right">매출액</th><th class="text-right">비중</th></tr>
    </thead>
    <tbody>"""

for i, (customer, amount) in enumerate(sorted(b2b_by_customer.items(), key=lambda x: x[1], reverse=True)[:10], 1):
    pct = amount / b2b_total * 100
    html += f"""
      <tr>
        <td>{i}</td>
        <td>{customer}</td>
        <td class="text-right">{fmt_full(amount)}원</td>
        <td class="text-right">{pct:.1f}%</td>
      </tr>"""

html += """
    </tbody>
  </table>
</div>

<!-- Insights -->
<div class="section">
  <h2>'그래서 뭐?' - 핵심 인사이트 3가지</h2>
  <div class="insight-grid">
    <div class="insight-card">
      <div class="number">INSIGHT 01</div>
      <div class="title">BLOEI 비데 = 성장 엔진 확인</div>
      <div class="desc">
        BLOEI 비데 발주량이 주차별로 급증 (1주차 대비 4주차 발주량 폭발적 증가).
        인테리어업체 중심 대량 발주가 이끌고, 대리점도 리오더 패턴 형성 중.
        <strong>문제: 재고일수 1.6일(일체형), 6.1일(일반형)</strong>으로 수요를 못 따라가고 있음.
      </div>
    </div>
    <div class="insight-card">
      <div class="number">INSIGHT 02</div>
      <div class="title">시공사 대물량이 매출 구조를 지배</div>
      <div class="desc">"""

html += f"""
        시공사 5개사 발주가 B2B 매출의 {b2b_by_type.get('시공사', 0)/b2b_total*100:.0f}%를 차지.
        대우건설/현대엔지니어링/GS건설/포스코이앤씨/호반건설 등 대형 현장이 한꺼번에 진행 중.
        봄 이사철 입주 물량 반영. 수전금구(CITY/MOD)와 위생도기 대량 소진 예상.
      </div>
    </div>
    <div class="insight-card">
      <div class="number">INSIGHT 03</div>
      <div class="title">온라인은 NeoTemp HOME이 견인</div>
      <div class="desc">
        온라인 채널에서 NeoTemp 수전 HOME(35만원)이 전체 온라인 매출의 상당 부분 차지.
        공식몰이 고단가 상품(NeoTemp, CANYON) 중심, 쿠팡은 CITY 수전 저단가 다량 판매 구조.
        온라인은 전체 매출의 {online_pct:.1f}%로 소규모이나, 브랜드 노출 채널로서 가치 있음.
      </div>
    </div>
  </div>
</div>

<!-- Action Items -->
<div class="section">
  <h2>봄 이사철 액션 아이템</h2>
  <div class="action-grid">
    <div class="action-card">
      <div class="tag">영업</div>
      <div class="title">BLOEI 비데 선주문 캠페인</div>
      <div class="desc">
        인테리어업체 5곳(카사/모던홈/리빙플러스/아뜰리에/스페이스랩)에 3-4월 물량 사전 확보 제안.
        현재 리오더 사이클이 2-3주로 짧아지는 추세 &mdash; 월 단위 선주문 계약으로 전환하면
        생산 계획 안정화 + 거래처 이탈 방지 가능.
        관공서 파이프라인(국방부/구청)도 조기 확정 필요.
      </div>
    </div>
    <div class="action-card">
      <div class="tag">온라인</div>
      <div class="title">NeoTemp HOME 단독 기획전</div>
      <div class="desc">
        공식몰 매출 견인 1위 상품. 쿠팡/네이버에도 프리미엄 포지셔닝 확대.
        BLOEI 비데 온라인 판매는 재고 확보 후 B2C 확장 검토 (현재는 B2B에 우선 배분).
        액세서리 3종세트가 네이버에서 꾸준한 매출 &mdash; 교차판매 번들 구성 고려.
      </div>
    </div>
    <div class="action-card">
      <div class="tag">재고/생산</div>
      <div class="title">긴급 생산 라인 BLOEI + CITY 집중</div>
      <div class="desc">
        BLOEI 비데 일체형(1.6일), NeoTemp SPA(2.7일), NeoTemp HOME(2.3일),
        세면수전 CITY(1.5일) &mdash; 4개 품목 즉시 증산.
        화성공장 비데 라인 가동률 확대 + 수전공장 NeoTemp/CITY 우선 배정.
        액세서리 3종세트(4.0일)도 추가 생산 필요 (온라인 판매 호조).
      </div>
    </div>
  </div>
</div>

<!-- Footer -->
<div style="text-align:center; padding:32px; color:#64748b; font-size:13px;">
  Royal 2026년 2월 전 채널 종합 보고서 | 데이터 기준: 2026-02-28 | 생성: Claude Code
</div>

</div>

<script>
// Chart.js defaults
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#334155';
Chart.defaults.font.family = "'Noto Sans KR', sans-serif";

// 1. B2B vs Online Pie
new Chart(document.getElementById('channelPie'), {{
  type: 'doughnut',
  data: {{
    labels: ['B2B (발주)', '온라인'],
    datasets: [{{
      data: [{b2b_total}, {online_total}],
      backgroundColor: ['#3b82f6', '#10b981'],
      borderColor: '#1e293b',
      borderWidth: 3,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ padding: 20 }} }},
      tooltip: {{
        callbacks: {{
          label: function(ctx) {{
            return ctx.label + ': ' + (ctx.raw / 100000000).toFixed(1) + '억원 (' + ((ctx.raw / {grand_total}) * 100).toFixed(1) + '%)';
          }}
        }}
      }}
    }},
    cutout: '60%'
  }}
}});

// 2. B2B Type Bar
new Chart(document.getElementById('b2bTypeBar'), {{
  type: 'bar',
  data: {{
    labels: {list(dict(sorted(b2b_by_type.items(), key=lambda x: x[1], reverse=True)).keys())},
    datasets: [{{
      data: {list(dict(sorted(b2b_by_type.items(), key=lambda x: x[1], reverse=True)).values())},
      backgroundColor: ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981'],
      borderRadius: 6,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      y: {{
        ticks: {{
          callback: function(v) {{ return (v / 100000000).toFixed(0) + '억'; }}
        }},
        grid: {{ color: '#1e293b' }}
      }},
      x: {{ grid: {{ display: false }} }}
    }}
  }}
}});

// 3. Online Channel Bar
new Chart(document.getElementById('onlineChannelBar'), {{
  type: 'bar',
  data: {{
    labels: {list(dict(sorted(online_by_channel.items(), key=lambda x: x[1], reverse=True)).keys())},
    datasets: [{{
      data: {list(dict(sorted(online_by_channel.items(), key=lambda x: x[1], reverse=True)).values())},
      backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
      borderRadius: 6,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      y: {{
        ticks: {{
          callback: function(v) {{ return (v / 10000).toFixed(0) + '만'; }}
        }},
        grid: {{ color: '#1e293b' }}
      }},
      x: {{ grid: {{ display: false }} }}
    }}
  }}
}});

// 4. BLOEI Trend
new Chart(document.getElementById('bloeiTrend'), {{
  type: 'line',
  data: {{
    labels: ['1주차', '2주차', '3주차', '4주차'],
    datasets: [
      {{
        label: '발주 수량',
        data: [{bloei_by_week['1주차']['qty']}, {bloei_by_week['2주차']['qty']}, {bloei_by_week['3주차']['qty']}, {bloei_by_week['4주차']['qty']}],
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointBackgroundColor: '#f59e0b',
        pointRadius: 6,
        yAxisID: 'y',
      }},
      {{
        label: '발주 금액',
        data: [{bloei_by_week['1주차']['amount']}, {bloei_by_week['2주차']['amount']}, {bloei_by_week['3주차']['amount']}, {bloei_by_week['4주차']['amount']}],
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointBackgroundColor: '#ef4444',
        pointRadius: 6,
        yAxisID: 'y1',
      }}
    ]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ padding: 16 }} }}
    }},
    scales: {{
      y: {{
        type: 'linear',
        display: true,
        position: 'left',
        title: {{ display: true, text: '수량 (개)' }},
        grid: {{ color: '#1e293b' }}
      }},
      y1: {{
        type: 'linear',
        display: true,
        position: 'right',
        title: {{ display: true, text: '금액' }},
        ticks: {{
          callback: function(v) {{ return (v / 100000000).toFixed(1) + '억'; }}
        }},
        grid: {{ drawOnChartArea: false }}
      }},
      x: {{ grid: {{ display: false }} }}
    }}
  }}
}});

// 5. Inventory Risk Chart
const invData = {[{'name': item['name'], 'days': item['stock_days'], 'color': '#ef4444' if item['stock_days'] < 7 else ('#f59e0b' if item['stock_days'] < 14 else '#10b981')} for item in sorted(inventory_items, key=lambda x: x['stock_days']) if item['category'] != '부자재']};
new Chart(document.getElementById('inventoryRisk'), {{
  type: 'bar',
  data: {{
    labels: invData.map(d => d.name),
    datasets: [{{
      data: invData.map(d => d.days),
      backgroundColor: invData.map(d => d.color),
      borderRadius: 4,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: function(ctx) {{ return '재고일수: ' + ctx.raw + '일'; }}
        }}
      }}
    }},
    scales: {{
      x: {{
        title: {{ display: true, text: '재고일수 (일)' }},
        grid: {{ color: '#1e293b' }}
      }},
      y: {{
        grid: {{ display: false }},
        ticks: {{ font: {{ size: 11 }} }}
      }}
    }}
  }}
}});
</script>
</body>
</html>"""

# Write HTML file
output_path = '/Users/rhim/Projects/do-better-workspace/50-resources/sample-data/royal_report_2602.html'
with open(output_path, 'w') as f:
    f.write(html)

# Print summary
print("=" * 60)
print("Royal 2026년 2월 전 채널 종합 보고서")
print("=" * 60)
print()
print(f"[핵심 숫자 3개]")
print(f"  1. 전 채널 합산 매출: {fmt_full(grand_total)}원 ({grand_total/100000000:.1f}억)")
print(f"  2. B2B vs 온라인: {b2b_pct:.1f}% vs {online_pct:.1f}%")
print(f"     - B2B: {fmt_full(b2b_total)}원")
print(f"     - 온라인: {fmt_full(online_total)}원")
print(f"  3. 거래처 유형별:")
for t, a in sorted(b2b_by_type.items(), key=lambda x: x[1], reverse=True):
    print(f"     - {t}: {fmt_full(a)}원 ({a/b2b_total*100:.1f}%)")
print()
print(f"[BLOEI 비데]")
print(f"  총 발주: {bloei_total_qty}개 / {fmt_full(bloei_total_amount)}원")
for week in ['1주차', '2주차', '3주차', '4주차']:
    d = bloei_by_week[week]
    print(f"  {week}: {d['qty']}개 / {fmt_full(d['amount'])}원")
print()
print(f"[재고 위험]")
print(f"  긴급 (7일 미만): {len(critical_items)}개 품목")
for item in sorted(critical_items, key=lambda x: x['stock_days']):
    print(f"    - {item['name']}: {item['stock_days']}일 (재고 {item['stock']}개)")
print(f"  주의 (14일 미만): {len(warning_items)}개 품목")
print()
print(f"[발주 취소] {fmt_full(cancelled_total)}원")
print(f"[온라인 취소/반품] {fmt_full(online_cancelled)}원")
print()
print(f"보고서 생성 완료: {output_path}")
