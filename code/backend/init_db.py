"""初始化数据库并写入示例数据"""
import sys
sys.path.insert(0, ".")

from app.database import engine, SessionLocal, Base
from app.models import Customer, Inquiry, Reply

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 检查是否已有数据
if db.query(Customer).first():
    print("数据库已有数据，跳过初始化")
    db.close()
    exit(0)

customers_data = [
    Customer(id="C001", name="Michael Johnson", company="Pacific Trading Co.",
             email="michael.j@pacific-trading.com", country="🇺🇸 USA, Los Angeles",
             level="A", status="following", source="email", priority="high",
             next_step="等待客户确认规格后发正式报价单", expected_close="1-2周"),
    Customer(id="C002", name="Emma Schmidt", company="Euro Retail GmbH",
             email="e.schmidt@euroretail.de", country="🇩🇪 Germany, Berlin",
             level="B", status="following", source="whatsapp", priority="medium",
             next_step="发送产品目录和报价单", expected_close="2-3周"),
    Customer(id="C003", name="Li Wei", company="Green Pack Asia",
             email="liwei@greenpack.asia", country="🇨🇳 China, Shanghai",
             level="B", status="pending", source="alibaba", priority="high",
             next_step="提供环保袋样品和认证资料", expected_close="1个月"),
    Customer(id="C004", name="Sarah Miller", company="Sunrise Hospitality",
             email="s.miller@sunrise-hosp.com", country="🇺🇸 USA, Miami",
             level="A", status="closed", source="email", priority="closed",
             next_step="已成交，交付中", expected_close="已成交"),
    Customer(id="C005", name="Ahmed Hassan", company="Dubai Hotel Group",
             email="ahmed.h@dubaihg.com", country="🇦🇪 UAE, Dubai",
             level="C", status="pending", source="email", priority="low",
             next_step="等待客户回复", expected_close="待定"),
]

for c in customers_data:
    db.add(c)

db.commit()
print(f"已写入 {len(customers_data)} 个客户")

# 询盘数据
from datetime import datetime, timedelta

inquiries_data = [
    Inquiry(customer_id="C001", channel="email", product="Paper Cups 50,000pcs",
            quantity="50,000 pcs", specs="12oz, food-grade, custom logo",
            destination="Los Angeles", intent="high",
            content="Hi, we are interested in your paper cups for our coffee shop chain. Could you send us the price for 50,000 pcs with custom logo? Please include sample options and delivery time to LA port.",
            status="following", summary="高意向客户，50k纸杯，FOB报价已发，等待确认规格"),
    Inquiry(customer_id="C002", channel="whatsapp", product="Custom Boxes 5,000",
            quantity="5,000 units", specs="custom printed",
            destination="Berlin", intent="medium",
            content="Hi, saw your products on Alibaba, want to know the price for 5000 units of custom printed boxes. Can you send a quote?",
            status="replied", summary="客户询定制彩盒，报价已发送"),
    Inquiry(customer_id="C003", channel="alibaba", product="Eco Bags 10,000",
            quantity="10,000 pcs", specs="biodegradable, custom logo",
            destination="Shanghai", intent="high",
            content="We are looking for eco-friendly bags supplier for our retail store. Need 10,000 pcs biodegradable bags, custom logo, delivery to Shanghai.",
            status="pending", summary="紧急询盘，生物降解袋，26h未回复"),
    Inquiry(customer_id="C004", channel="email", product="Paper Napkins 20,000pcs",
            quantity="20,000 pcs", specs="food grade, custom printing",
            destination="Miami", intent="high",
            content="Need 20,000 pcs paper napkins with custom printing, food grade material. Please quote FOB Shanghai price.",
            status="closed", summary="已成交，首单确认，30%定金已收"),
    Inquiry(customer_id="C005", channel="email", product="Paper Cups 30,000",
            quantity="30,000 pcs", specs="hotel grade",
            destination="Dubai", intent="medium",
            content="Hello, we need 30,000 pcs paper cups for our hotel chain in Dubai. Please provide best FOB price and delivery time.",
            status="pending", summary="迪拜酒店集团，30k纸杯，26h未回复"),
]

for i in inquiries_data:
    db.add(i)

db.commit()
print(f"已写入 {len(inquiries_data)} 条询盘")

# 回复数据
replies_data = [
    Reply(inquiry_id=1, content="Dear Michael, Thank you for your inquiry. FOB price: USD 0.12/pc for 50,000 pcs. Sample: 5-7 days, fee refundable upon order. We accept T/T and L/C at sight."),
    Reply(inquiry_id=1, content="Dear Michael, Following up on our previous email. Just wanted to confirm if you have reviewed the quotation. We also have FSC certified materials available."),
    Reply(inquiry_id=2, content="Hi Emma, Thanks for reaching out! Custom boxes for 5000 units would be approximately USD 0.85/pc. I will send the full quotation sheet shortly."),
    Reply(inquiry_id=4, content="Dear Sarah, Our paper napkins at 20,000 pcs with custom printing would be USD 0.05/pc FOB Shanghai."),
    Reply(inquiry_id=4, content="Order confirmed! We've received your deposit. Production will start next week. Estimated delivery: 20-25 days."),
]

for r in replies_data:
    db.add(r)

db.commit()
print(f"已写入 {len(replies_data)} 条回复")
print("数据库初始化完成 ✅")

db.close()
