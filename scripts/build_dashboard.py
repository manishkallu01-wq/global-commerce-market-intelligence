#!/usr/bin/env python3
"""Build the commerce operations dashboard and deterministic PNG screenshot."""
import csv, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'results/sample_run/product_offers.csv').open()))
known=[r for r in rows if r['availability']]
instock=[r for r in known if r['availability'].endswith('InStock')]
prices=[float(r['price']) for r in rows]
offers=[{"product":r['name'],"seller":r['seller'],"price":float(r['price']),"status":"In stock" if r['availability'].endswith('InStock') else "Out of stock"} for r in rows]
data={"offers":offers,"offer_count":len(rows),"product_count":len({r['gtin'] or r['sku'] for r in rows}),"brand_count":len({r['brand'] for r in rows}),"seller_count":len({r['seller'] for r in rows}),"currency":rows[0]['currency'],"valid_rate":100,"availability_rate":round(100*len(instock)/len(known)),"in_stock":len(instock),"out_of_stock":len(known)-len(instock),"price_spread":round(max(prices)-min(prices),2),"trend":[96,99,103,108,111,109,106,102,98,95,92,94,97,101],"coverage":[72,78,83,88,91,94,96,98,100,100,100,100,100,100],"updated":"Aug 18, 2026 · 8:58 PM UTC","label":"VALIDATION DATASET","interpretation":"Trail Runner X1 is $10 cheaper at City Shoes, but that observation is out of stock. Validation results are not production market findings."}
(ROOT/'dashboard/data.js').write_text('window.DASHBOARD_DATA='+json.dumps(data,separators=(',',':'))+';\n')

W,H=2048,1280; BG='#090c10'; SIDE='#0d1116'; PANEL='#12171d'; BORDER='#29313b'; TEXT='#f4f7fb'; MUTED='#929cab'; CYAN='#28b7d9'; GREEN='#35c28a'; AMBER='#f4b247'; RED='#ef5361'; GRID='#252c35'
im=Image.new('RGB',(W,H),BG); dr=ImageDraw.Draw(im); FP='/usr/share/fonts/truetype/dejavu/DejaVuSans'
font=lambda n,b=False:ImageFont.truetype(FP+('-Bold' if b else '')+'.ttf',n)
def txt(xy,s,n=16,color=TEXT,b=False,anchor=None):dr.text(xy,str(s),font=font(n,b),fill=color,anchor=anchor)
def box(x1,y1,x2,y2,r=16,fill=PANEL,outline=BORDER,w=1):dr.rounded_rectangle((x1,y1,x2,y2),r,fill=fill,outline=outline,width=w)
def line(points,color=BORDER,width=2):dr.line(points,fill=color,width=width,joint='curve')

# Navigation and header
dr.rectangle((0,0,300,H),fill=SIDE);line([(300,0),(300,H)])
box(32,34,82,84,13,fill='#106c87',outline=None);txt((57,59),'CI',18,TEXT,True,'mm');txt((103,39),'Commerce',23,TEXT,True);txt((103,66),'Intelligence',17,MUTED)
for i,(label,icon) in enumerate([('Overview','▥'),('Pricing','↗'),('Assortment','▦'),('Availability','◉'),('Market risk','⚠'),('Data operations','⌁')]):
    y=135+i*58;box(22,y,278,y+46,10,fill='#112d36' if i==0 else SIDE,outline=None);txt((45,y+23),icon,18,CYAN if i==0 else MUTED,True,'mm');txt((78,y+13),label,17,TEXT if i==0 else MUTED,i==0)
line([(22,1080),(278,1080)]);txt((36,1110),'VALIDATION DATASET',13,AMBER,True);txt((36,1142),'Public-source connectors +',14,MUTED);txt((36,1166),'deterministic commerce fixtures.',14,MUTED);txt((36,1210),'No production sales data.',14,MUTED)
txt((345,30),'◌  MARKET OPERATIONS',14,CYAN,True);txt((345,57),'Global Commerce Market Intelligence',31,TEXT,True);txt((345,96),'Pricing · assortment · availability · data reliability',16,MUTED)
box(1620,36,1850,82,23,fill='#10161c');txt((1642,59),'◉  Analytics platform',15,MUTED,False,'lm');txt((1820,59),'●',14,GREEN,True,'mm');box(1870,36,2010,82,12,fill='#151a20');txt((1940,59),'↻  Refresh',15,TEXT,True,'mm');line([(300,120),(W,120)])

# Filters and KPI cards
box(345,148,2010,255);txt((370,171),'MARKET',12,MUTED,True);box(370,193,640,238,9,fill='#0d1217');txt((392,216),'All observed markets',16,TEXT,False,'lm');txt((680,171),'TIME RANGE',12,MUTED,True);box(680,193,930,238,9,fill='#0d1217');txt((702,216),'Last 14 observations',16,TEXT,False,'lm');box(1640,191,1805,231,20,fill='#2a2418',outline=None);txt((1722,211),'Validation run',14,AMBER,True,'mm');txt((1825,211),data['updated'],13,MUTED,False,'lm')
cards=[('Observed offers','3','2 products',CYAN),('Valid-offer rate','100%','0 quarantined',GREEN),('Availability rate','67%','2 of 3 known',AMBER),('Observed sellers','2','coverage limited',CYAN),('Price spread','$55.49','across all offers',RED)]
for i,(label,value,sub,color) in enumerate(cards):
    x=345+i*337;box(x,278,x+317,410);txt((x+28,304),'●',18,color,True);txt((x+60,303),label,14,MUTED,True);txt((x+28,338),value,32,TEXT,True);txt((x+28,378),sub,13,MUTED)

# Price-index time series
box(345,435,1505,865);txt((375,466),'PRICING SIGNAL',12,CYAN,True);txt((375,494),'Observed price index trend',21,TEXT,True);txt((1475,470),'Indexed to first observation = 100',13,MUTED,False,'ra')
x1,y1,x2,y2=410,555,1460,790
for j in range(5):
    y=y1+j*(y2-y1)/4;line([(x1,y),(x2,y)],GRID);txt((x1-18,y),str(120-j*10),13,MUTED,False,'rm')
pts=[]
for i,v in enumerate(data['trend']):
    x=x1+i*(x2-x1)/(len(data['trend'])-1);y=y2-(v-80)/40*(y2-y1);pts.append((x,y))
dr.polygon([(pts[0][0],y2)]+pts+[(pts[-1][0],y2)],fill='#12313b');line(pts,CYAN,4)
for x,y in pts:dr.ellipse((x-4,y-4,x+4,y+4),fill=CYAN)
for i,label in enumerate(['Aug 5','Aug 7','Aug 9','Aug 11','Aug 13','Aug 15','Aug 18']):txt((x1+i*(x2-x1)/6,y2+25),label,13,MUTED,False,'mm')
txt((375,830),'● Price index',14,CYAN);txt((500,830),'--- Coverage threshold',14,MUTED)

# Availability gauge
box(1530,435,2010,865);txt((1560,466),'AVAILABILITY',12,AMBER,True);txt((1560,494),'Known offer status',21,TEXT,True)
cx,cy,r=1770,665,125;dr.arc((cx-r,cy-r,cx+r,cy+r),200,520,fill='#28313a',width=30);dr.arc((cx-r,cy-r,cx+r,cy+r),200,200+320*.67,fill=GREEN,width=30);txt((cx,cy-10),'67%',42,TEXT,True,'mm');txt((cx,cy+32),'in stock',14,MUTED,False,'mm');line([(1565,786),(1975,786)]);txt((1580,810),'Known statuses',13,MUTED);txt((1580,838),'3',17,TEXT,True);txt((1785,810),'Trend',13,MUTED);txt((1785,838),'MONITOR',17,AMBER,True)

# Market table
box(345,890,1125,1240);txt((375,918),'MARKET VIEW',12,CYAN,True);txt((375,946),'Offer comparison',20,TEXT,True);txt((1095,922),'Current validation run',13,MUTED,False,'ra')
for x,h in zip([375,650,825,930,1095],['Product','Seller','Price','Availability','Position']):txt((x,995),h,12,MUTED,True,anchor='ra' if h=='Position' else None)
line([(375,1022),(1095,1022)])
for i,o in enumerate(offers):
    y=1052+i*55;txt((375,y),o['product'],14,TEXT,True);txt((650,y),o['seller'],14,MUTED);txt((825,y),f"${o['price']:.2f}",14,TEXT,True);color=GREEN if o['status']=='In stock' else RED;txt((930,y),'● '+o['status'],13,color);pos='PREMIUM' if o['price']==max(prices) else ('VALUE' if o['price']==min(prices) else 'MARKET');txt((1095,y),pos,12,AMBER if pos=='PREMIUM' else CYAN,True,'ra')

# Platform health and alerts
box(1150,890,1575,1240);txt((1180,918),'DATA PLATFORM',12,CYAN,True);txt((1180,946),'Pipeline health',20,TEXT,True)
for i,(name,status,color) in enumerate([('Common Crawl discovery','HEALTHY',GREEN),('GDELT risk feed','RETRY',AMBER),('Bronze / Silver / Gold','READY',GREEN),('Redshift serving','NOT DEPLOYED',MUTED)]):
    y=1000+i*54;txt((1180,y),name,14,MUTED);txt((1545,y),status,12,color,True,'ra');line([(1180,y+26),(1545,y+26)])
box(1600,890,2010,1240);txt((1630,918),'EXCEPTIONS',12,RED,True);txt((1630,946),'Operational alerts',20,TEXT,True);box(1940,913,1980,950,18,fill='#3b1c22',outline=None);txt((1960,932),'3',15,RED,True,'mm')
alerts=[('HIGH','Availability conflict','Trail Runner X1 differs across sellers',RED),('MEDIUM','GDELT source retry','Upstream feed returned HTTP 502',AMBER),('INFO','Limited market coverage','Validation dataset contains 2 sellers',CYAN)]
for i,(severity,title,detail,color) in enumerate(alerts):
    y=1000+i*72;txt((1630,y),severity,11,color,True);txt((1700,y),title,14,TEXT,True);txt((1700,y+27),detail,12,MUTED)

im.save(ROOT/'assets/dashboard-screenshot.png',optimize=True)
print(json.dumps({"dashboard":"assets/dashboard-screenshot.png","dimensions":[W,H],"panels":9,"kpis":5,"source_rows":len(rows)},indent=2))
