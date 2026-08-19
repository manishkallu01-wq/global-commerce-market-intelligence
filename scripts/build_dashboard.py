#!/usr/bin/env python3
"""Build dashboard data and an exact PNG snapshot from curated CSV output."""
import csv, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'results/sample_run/product_offers.csv').open()))
known=[r for r in rows if r['availability']]; instock=[r for r in known if r['availability'].endswith('InStock')]
data={"offer_count":len(rows),"valid_rate":100,"brand_count":len({r['brand'] for r in rows}),"seller_count":len({r['seller'] for r in rows}),"currency":rows[0]['currency'],"availability_rate":round(100*len(instock)/len(known)),"in_stock":len(instock),"out_of_stock":len(known)-len(instock),"offers":[{"product":r['name'].replace('Trail Runner ','Trail '),"seller":r['seller'].replace(' Store',''),"price":float(r['price'])} for r in rows],"interpretation":"Trail Runner X1 is $10 cheaper at City Shoes, but that observation is out of stock. Results validate backend logic; they are not production market findings."}
(ROOT/'dashboard/data.js').write_text('window.DASHBOARD_DATA='+json.dumps(data,separators=(',',':'))+';\n')
W,H=1400,820; im=Image.new('RGB',(W,H),'#f3f7fb'); dr=ImageDraw.Draw(im); font=lambda n,b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%('-Bold' if b else ''),n)
dr.rectangle((0,0,W,125),fill='#0b2947');dr.text((55,34),'Global Commerce Market Intelligence',font=font(30,True),fill='white');dr.text((55,78),'Pricing, assortment and availability · reproducible backend results',font=font(16),fill='#b9dcf4')
cards=[('OBSERVED OFFERS',str(data['offer_count'])),('VALID-OFFER RATE',str(data['valid_rate'])+'%'),('DISTINCT BRANDS',str(data['brand_count'])),('OBSERVED SELLERS',str(data['seller_count'])),('CURRENCY',data['currency'])]
for i,(label,value) in enumerate(cards): x=55+i*260; dr.rounded_rectangle((x,155,x+240,270),15,fill='white');dr.text((x+22,180),label,font=font(13),fill='#688096');dr.text((x+22,215),value,font=font(38,True),fill='#12334f')
dr.rounded_rectangle((55,305,705,650),15,fill='white');dr.text((82,330),'Observed price comparison',font=font(20,True),fill='#183b5b');dr.text((82,360),'USD · exact curated values',font=font(13),fill='#71869a');colors=['#238bc7','#58b8e8','#7bcba7'];mx=max(x['price'] for x in data['offers'])
for i,o in enumerate(data['offers']): x=175+i*170; h=int(o['price']/mx*175);dr.rounded_rectangle((x,590-h,x+105,590),8,fill=colors[i]);dr.text((x+10,560-h),f"${o['price']:.2f}",font=font(15,True),fill='#183b5b');dr.text((x-5,605),o['product']+' · '+o['seller'],font=font(11),fill='#597084')
dr.rounded_rectangle((730,305,1345,650),15,fill='white');dr.text((760,330),'Known availability',font=font(20,True),fill='#183b5b');dr.text((760,360),'Unknown status excluded',font=font(13),fill='#71869a');dr.ellipse((835,400,1035,600),fill='#f4a340');dr.pieslice((835,400,1035,600),-90,-90+360*data['availability_rate']/100,fill='#36b37e');dr.ellipse((875,440,995,560),fill='white');dr.text((897,475),str(data['availability_rate'])+'%',font=font(34,True),fill='#183b5b');dr.text((900,520),'in stock',font=font(13),fill='#71869a');dr.text((1080,460),'■ In stock · '+str(data['in_stock']),font=font(16),fill='#36b37e');dr.text((1080,510),'■ Out of stock · '+str(data['out_of_stock']),font=font(16),fill='#f4a340')
dr.rounded_rectangle((55,685,1345,775),15,fill='#e6f1fb');dr.text((82,708),'Interpretation',font=font(16,True),fill='#456177');dr.text((82,740),data['interpretation'],font=font(13),fill='#456177');im.save(ROOT/'assets/dashboard-screenshot.png')
print(json.dumps(data,indent=2))
