<template>
  <div class="layout">

    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">📊 <span>销售系统</span></div>
      <nav class="nav">
        <div class="nav-item active">
          <span class="icon">📊</span><span class="txt">仪表盘</span>
        </div>
        <div class="nav-item">
          <span class="icon">📋</span><span class="txt">询盘管理</span>
        </div>
        <div class="nav-item">
          <span class="icon">👥</span><span class="txt">客户管理</span>
        </div>
        <div class="nav-item">
          <span class="icon">📦</span><span class="txt">订单管理</span>
        </div>
        <div class="nav-item">
          <span class="icon">⚙️</span><span class="txt">系统设置</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容 -->
    <div class="main">

      <!-- 顶栏 -->
      <header class="topbar">
        <div class="topbar-left">
          <div class="page-title">销售仪表盘</div>
          <div class="page-sub">实时追踪三个渠道的询盘转化情况</div>
        </div>
        <div class="topbar-right">
          <div class="search-bar">
            <span class="search-icon">🔍</span>
            <input placeholder="搜索客户、产品..." v-model="searchKw" />
          </div>
          <div class="notif-btn">🔔<span v-if="alertCount" class="notif-dot">{{ alertCount }}</span></div>
          <div class="user-avatar">白</div>
        </div>
      </header>

      <!-- 主体 -->
      <div class="content">

        <!-- 左侧：仪表盘 -->
        <div class="left">

          <!-- 统计卡片 -->
          <div class="stats">
            <div class="stat" v-for="s in stats" :key="s.label">
              <div class="stat-icon" :style="{ background: s.bg }">{{ s.icon }}</div>
              <div class="stat-info">
                <div class="stat-label">{{ s.label }}</div>
                <div class="stat-value" :class="s.valueClass">{{ s.value }}</div>
                <div class="stat-sub" :class="s.subClass">{{ s.sub }}</div>
              </div>
            </div>
          </div>

          <!-- 图表 -->
          <div class="charts">
            <div class="card chart-card line-card">
              <div class="card-title-row">
                <div class="card-title">📈 询盘趋势</div>
                <div class="seg-btns">
                  <button :class="{ active: trendRange === '7d' }" @click="trendRange = '7d'">7天</button>
                  <button :class="{ active: trendRange === '30d' }" @click="trendRange = '30d'">30天</button>
                </div>
              </div>
              <div ref="lineChartRef" style="height:180px;margin-top:12px"></div>
            </div>
            <div class="card chart-card pie-card">
              <div class="card-title-row">
                <div class="card-title">📊 渠道分布</div>
              </div>
              <div ref="pieChartRef" style="height:180px;margin-top:12px"></div>
            </div>
          </div>

          <!-- 漏斗+超时 -->
          <div class="bottom-cards">
            <div class="card funnel-card">
              <div class="card-title">🔃 转化漏斗</div>
              <div class="funnel">
                <div class="f-step" v-for="(f, i) in funnel" :key="i">
                  <div class="f-left">
                    <span class="f-label">{{ f.label }}</span>
                    <span class="f-bar-bg">
                      <span class="f-bar-fill" :style="{ width: f.pct + '%', background: f.color }"></span>
                    </span>
                  </div>
                  <div class="f-right">
                    <span class="f-num">{{ f.num }}</span>
                    <span class="f-pct" v-if="f.pct">{{ f.pct }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="card alert-card">
              <div class="card-title">⚠️ 超时待处理 <span class="badge-red">{{ alerts.length }}</span></div>
              <div class="alert-list">
                <div class="alert-item" v-for="a in alerts" :key="a.id">
                  <span class="a-ch">{{ chIcon(a.channel) }}</span>
                  <div class="a-info">
                    <div class="a-name">{{ a.customer }}</div>
                    <div class="a-pro">{{ a.product }}</div>
                  </div>
                  <div class="a-overdue">{{ a.overdue }}未回复</div>
                </div>
                <div v-if="!alerts.length" class="a-ok">暂无超时 👍</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：询盘列表 -->
        <div class="right">
          <div class="card inq-card">
            <div class="card-title-row">
              <div class="card-title">📋 询盘列表 <span class="cnt">{{ filtered.length }} 条</span></div>
              <div class="flt">
                <select v-model="fChannel" class="fsel">
                  <option value="">全部渠道</option>
                  <option value="email">📧 邮件</option>
                  <option value="whatsapp">💬 WhatsApp</option>
                  <option value="alibaba">🛒 阿里站</option>
                </select>
                <select v-model="fStatus" class="fsel">
                  <option value="">全部状态</option>
                  <option value="pending">⏳ 待回复</option>
                  <option value="replied">✅ 已回复</option>
                  <option value="following">🔄 跟进中</option>
                  <option value="closed">🏁 已成交</option>
                  <option value="invalid">⚫ 无效</option>
                </select>
              </div>
            </div>

            <div class="inq-scroll">
              <div
                v-for="item in filtered"
                :key="item.id"
                class="inq-item"
                :class="{ 'is-danger': item.overHours > 24 }"
                @click="$router.push('/inquiry/' + item.id)"
              >
                <div class="inq-row">
                  <span class="inq-ch">{{ chIcon(item.channel) }}</span>
                  <div class="inq-info">
                    <div class="inqname">{{ item.customer }}</div>
                    <div class="inqpro">{{ item.product }}</div>
                  </div>
                  <div class="inq-right">
                    <div class="inq-time">{{ item.time }}</div>
                    <div class="inq-st" :class="'st-' + item.status">{{ stLabel(item.status) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getStats, getInquiries } from '../api'
import * as echarts from 'echarts'

// 响应式数据
const trendRange = ref('7d')
const searchKw = ref('')
const fChannel = ref('')
const fStatus = ref('')
const router = useRouter()

const expId = ref(null)
const lineChartRef = ref(null)
const pieChartRef = ref(null)

// 工具函数
const chIcon = (c) => ({ email:'📧', whatsapp:'💬', alibaba:'🛒' }[c] || '📌')
const stLabel = (s) => ({ pending:'待回复', replied:'已回复', following:'跟进中', closed:'已成交', invalid:'无效' }[s] || s)
// 静态数据（后续替换为 API 调用）
const stats = ref([
  { label:'今日询盘', value:0, sub:'加载中...', icon:'📬', bg:'#EEF2FF', valueClass:'', subClass:'' },
  { label:'本周询盘', value:0, sub:'加载中...', icon:'💬', bg:'#F0FDF4', valueClass:'', subClass:'' },
  { label:'待回复', value:0, sub:'加载中...', icon:'⚠️', bg:'#FEF3C7', valueClass:'red', subClass:'warn' },
  { label:'本月成交', value:0, sub:'加载中...', icon:'✅', bg:'#ECFDF5', valueClass:'', subClass:'' },
])

const funnel = ref([
  { label:'收到询盘', num:0, pct:null, color:'#94A3B8' },
  { label:'已回复', num:0, pct:75, color:'#60A5FA' },
  { label:'跟进中', num:0, pct:27, color:'#FBBF24' },
  { label:'已成交', num:0, pct:12, color:'#34D399' },
])

const alerts = ref([])

const inquiries = ref([
  { id:1, channel:'email', customer:'Michael Johnson', product:'Paper Cups 50,000pcs',
    content:'Hi, we are interested in your paper cups for our coffee shop chain. Could you send us the price for 50,000 pcs with custom logo? Please include sample options and delivery time to LA port.',
    time:'2小时前', status:'following', overHours:5,
    replies:[
      { time:'2026-03-30 14:30', content:'Dear Michael, Thank you for your inquiry. FOB price: USD 0.12/pc for 50,000 pcs. Sample: 5-7 days, fee refundable upon order.' },
      { time:'2026-03-30 16:45', content:'Dear Michael, Following up on our previous email. Just wanted to confirm if you have reviewed the quotation.' },
    ]},
  { id:2, channel:'whatsapp', customer:'Emma Schmidt', product:'Custom Boxes 5,000',
    content:'Hi, saw your products on Alibaba, want to know the price for 5000 units of custom printed boxes. Can you send a quote?',
    time:'5小时前', status:'replied', overHours:0,
    replies:[{ time:'2026-03-31 10:15', content:'Hi Emma, Thanks for reaching out! Custom boxes for 5000 units would be approximately USD 0.85/pc.' }]},
  { id:3, channel:'alibaba', customer:'Li Wei', product:'Eco Bags 10,000',
    content:'We are looking for eco-friendly bags supplier for our retail store. Need 10,000 pcs biodegradable bags, custom logo, delivery to Shanghai.',
    time:'1天前', status:'pending', overHours:26, replies:[] },
  { id:4, channel:'email', customer:'Sarah Miller', product:'Paper Napkins 20,000pcs',
    content:'Need 20,000 pcs paper napkins with custom printing, food grade material. Please quote FOB Shanghai price.',
    time:'1天前', status:'closed', overHours:0,
    replies:[
      { time:'2026-03-29 09:00', content:"Dear Sarah, Our paper napkins at 20,000 pcs with custom printing would be USD 0.05/pc FOB Shanghai." },
      { time:'2026-03-29 11:30', content:"Order confirmed! We've received your deposit. Production will start next week." },
    ]},
  { id:5, channel:'email', customer:'Ahmed Hassan', product:'Paper Cups 30,000',
    content:'Hello, we need 30,000 pcs paper cups for our hotel chain in Dubai. Please provide best FOB price and delivery time.',
    time:'2天前', status:'pending', overHours:26, replies:[] },
  { id:6, channel:'whatsapp', customer:'Maria Garcia', product:'Paper Straws 8,000',
    content:'Hi, interested in paper straws for our restaurant. Need mixed colors, 8,000 pcs. Price and sample info please?',
    time:'3天前', status:'following', overHours:0,
    replies:[{ time:'2026-03-29 15:00', content:'Hi Maria! Paper straws at 8,000 pcs: USD 0.03/pc. Mixed colors available. Samples can be sent within 3 days.' }]},
  { id:7, channel:'alibaba', customer:'Chen Wei', product:'Pizza Boxes 3,000',
    content:'Looking for supplier for custom printed pizza boxes, 12 inch size, 3,000 pcs. Please quote.',
    time:'4天前', status:'invalid', overHours:0,
    replies:[{ time:'2026-03-27 10:00', content:'Hi Chen Wei, Unfortunately our minimum order quantity is 5,000 pcs for custom pizza boxes.' }]},
])

const filtered = computed(() =>
  inquiries.value.filter(i => {
    if (fChannel.value && i.channel !== fChannel.value) return false
    if (fStatus.value && i.status !== fStatus.value) return false
    return true
  })
)

const alertCount = computed(() => alerts.length)

// ECharts 实例
let lineChart = null
let pieChart = null

onMounted(async () => {
  // 加载 API 数据
  try {
    const [statsData, inqData] = await Promise.all([
      getStats(),
      getInquiries()
    ])
    stats.value = [
      { label:'今日询盘', value:statsData.today_inquiries, sub:'今日新增', icon:'📬', bg:'#EEF2FF', valueClass:'', subClass:'up' },
      { label:'本周询盘', value:statsData.week_inquiries, sub:'本周合计', icon:'💬', bg:'#F0FDF4', valueClass:'', subClass:'up' },
      { label:'待回复', value:statsData.pending, sub:'需尽快处理', icon:'⚠️', bg:'#FEF3C7', valueClass: statsData.pending > 0 ? 'red' : '', subClass: statsData.pending > 0 ? 'warn' : '' },
      { label:'本月成交', value:statsData.closed, sub:'已成交', icon:'✅', bg:'#ECFDF5', valueClass:'', subClass:'up' },
    ]
    inquiries.value = inqData.map(i => ({
      ...i,
      time: new Date(i.created_at).toLocaleString('zh-CN', { month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' }),
      overHours: Math.floor((Date.now() - new Date(i.created_at)) / 3600000),
    }))
    funnel.value[0].num = inqData.length
    funnel.value[1].num = inqData.filter(i => ['replied','following','closed'].includes(i.status)).length
    funnel.value[2].num = inqData.filter(i => i.status === 'following').length
    funnel.value[3].num = inqData.filter(i => i.status === 'closed').length
    alerts.value = inqData.filter(i => i.status === 'pending' && Math.floor((Date.now() - new Date(i.created_at)) / 3600000) > 24)
      .slice(0, 5)
      .map(i => ({ id:i.id, channel:i.channel, customer:i.customer?.name || '未知', product:i.product, overdue:Math.floor((Date.now() - new Date(i.created_at)) / 3600000) + 'h' }))
  } catch (e) {
    console.error('API加载失败:', e)
  }

  // 初始化折线图
  lineChart = echarts.init(lineChartRef.value)
  lineChart.setOption({
    tooltip:{ trigger:'axis' },
    legend:{ data:['📧 邮件','💬 WhatsApp','🛒 阿里站'], bottom:0, textStyle:{ fontSize:11, fontFamily:'Inter' } },
    grid:{ top:4, bottom:36, left:36, right:8 },
    xAxis:{ type:'category',
      data:['周一','周二','周三','周四','周五','周六','周日'],
      axisLine:{ lineStyle:{ color:'#E5E7EB' } },
      axisLabel:{ fontSize:11, color:'#9CA3AF' } },
    yAxis:{ type:'value',
      splitLine:{ lineStyle:{ color:'#F3F4F6' } },
      axisLine:{ show:false }, axisTick:{ show:false },
      axisLabel:{ fontSize:11, color:'#9CA3AF' } },
    series:[
      { name:'📧 邮件', type:'line', smooth:true, data:[12,15,18,14,20,22,18], symbol:'circle', symbolSize:6,
        lineStyle:{ color:'#3B82F6', width:2 }, itemStyle:{ color:'#3B82F6' },
        areaStyle:{ color:'#EEF2FF', origin:'start' } },
      { name:'💬 WhatsApp', type:'line', smooth:true, data:[8,10,12,9,14,16,13], symbol:'circle', symbolSize:6,
        lineStyle:{ color:'#22C55E', width:2 }, itemStyle:{ color:'#22C55E' },
        areaStyle:{ color:'#F0FDF4', origin:'start' } },
      { name:'🛒 阿里站', type:'line', smooth:true, data:[5,7,9,8,11,13,10], symbol:'circle', symbolSize:6,
        lineStyle:{ color:'#F97316', width:2 }, itemStyle:{ color:'#F97316' },
        areaStyle:{ color:'#FFF7ED', origin:'start' } },
    ]
  })

  // 初始化饼图
  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip:{ trigger:'item' },
    legend:{ orient:'vertical', right:4, top:16, textStyle:{ fontSize:11, color:'#6B7280' } },
    series:[{
      type:'pie', radius:['55%','80%'], center:['35%','50%'],
      label:{ show:false },
      data:[
        { value:68, itemStyle:{ color:'#3B82F6' } },
        { value:51, itemStyle:{ color:'#22C55E' } },
        { value:37, itemStyle:{ color:'#F97316' } },
      ]
    }]
  })

  // 响应窗口 resize，带清理
  const handleResize = () => {
    lineChart?.resize()
    pieChart?.resize()
  }
  window.addEventListener('resize', handleResize)

  // 清理：组件卸载时移除监听，防止内存泄漏
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    lineChart?.dispose()
    pieChart?.dispose()
  })
})
</script>

<style scoped>
/* ============================================
   规范：frontend-design-ultimate + anthropics/skills@frontend-design
   字体：Plus Jakarta Sans(标题) + DM Sans(正文)
   ============================================ */

/* CSS 变量系统 */
:root {
  --bg: #F4F5F8;
  --surface: #FFFFFF;
  --border: #E5E7EB;
  --text-h: #111827;
  --text-m: #374151;
  --text-c: #6B7280;
  --text-f: #9CA3AF;
  --primary: #2563EB;
  --primary-hover: #1D4ED8;
  --sidebar-bg: #1E293B;
  --sidebar-text: rgba(255,255,255,0.55);
  --sidebar-text-active: #FFFFFF;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --shadow-md: 0 2px 12px rgba(0,0,0,0.08);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: 0.15s ease;
}

/* 重置 */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body,#app{height:100%;overflow:hidden}

body{
  font-family:'DM Sans','Noto Sans SC',system-ui,sans-serif;
  background:var(--bg);
  color:var(--text-h);
  font-size:14px;
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  /* 细腻噪点纹理（规范要求：背景要有氛围感，不是纯色） */
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
}

/* Focus 可见性（可访问性规范要求） */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 4px;
}
:focus:not(:focus-visible) { outline: none; }

/* 整体 */
.layout{display:flex;height:100vh;overflow:hidden;width:100vw;max-width:100vw}

/* 侧边栏 */
.sidebar{width:180px;background:var(--sidebar-bg);display:flex;flex-direction:column;flex-shrink:0}
.logo{
  display:flex;align-items:center;gap:10px;
  padding:0 20px;height:64px;
  border-bottom:1px solid rgba(255,255,255,0.06);
  color:#fff;font-size:18px;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:700
}
.logo span{font-size:13px;font-weight:700}
.nav{display:flex;flex-direction:column;padding:12px 0;gap:2px}
.nav-item{
  display:flex;align-items:center;
  padding:10px 20px;cursor:pointer;
  color:var(--sidebar-text);font-size:13px;gap:10px;
  transition:background var(--transition),color var(--transition);
  border-radius:0;
}
.nav-item:hover{color:var(--sidebar-text-active);background:rgba(255,255,255,0.06)}
.nav-item.active{color:var(--sidebar-text-active);background:rgba(37,99,235,0.55)}
.icon{font-size:16px;flex-shrink:0}

/* 主区 */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* 顶栏 */
.topbar{
  height:64px;background:var(--surface);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;flex-shrink:0
}
.topbar-left{display:flex;flex-direction:column;justify-content:center}
.page-title{
  font-size:18px;font-weight:700;color:var(--text-h);
  font-family:'Plus Jakarta Sans',sans-serif
}
.page-sub{font-size:12px;color:var(--text-f);margin-top:1px}
.topbar-right{display:flex;align-items:center;gap:16px}
.search-bar{
  display:flex;align-items:center;gap:8px;
  background:var(--bg);border:1px solid var(--border);
  border-radius:var(--radius-sm);padding:7px 12px;
  transition:border-color var(--transition),box-shadow var(--transition);
}
.search-bar:focus-within{
  border-color:var(--primary);
  box-shadow:0 0 0 3px rgba(37,99,235,0.1);
}
.search-bar input{background:none;border:none;outline:none;font-size:13px;color:var(--text-m);width:200px;font-family:inherit}
.search-bar input::placeholder{color:var(--text-f)}
.notif-btn{position:relative;cursor:pointer;font-size:20px;padding:4px;transition:opacity var(--transition)}
.notif-btn:hover{opacity:0.7}
.notif-dot{
  position:absolute;top:-2px;right:-2px;
  width:14px;height:14px;background:#EF4444;color:#fff;
  border-radius:50%;font-size:9px;
  display:flex;align-items:center;justify-content:center;font-weight:700;line-height:1
}
.user-avatar{
  width:36px;height:36px;background:var(--primary);color:#fff;
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-weight:600;font-size:13px;
  font-family:'Plus Jakarta Sans',sans-serif;
  cursor:pointer;transition:opacity var(--transition),transform var(--transition);
}
.user-avatar:hover{opacity:0.85;transform:scale(1.05)}

/* 内容 */
.content{display:flex;flex:1;overflow:hidden;gap:14px;padding:14px 16px 16px}

/* 左侧 */
.left{flex:1;display:flex;flex-direction:column;gap:14px;overflow-y:auto;min-width:0}

/* 右侧 */
.right{width:380px;flex-shrink:0;overflow:hidden;display:flex;flex-direction:column}

/* 卡片 */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:box-shadow var(--transition)}
.card:hover{box-shadow:var(--shadow-md)}

/* 统计 */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:20px;display:flex;align-items:center;gap:16px;
  transition:box-shadow var(--transition),transform var(--transition);
}
.stat:hover{box-shadow:var(--shadow-md);transform:translateY(-1px)}
.stat-icon{
  width:48px;height:48px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0
}
.stat-info{flex:1;min-width:0}
.stat-label{font-size:12px;color:var(--text-c);font-weight:500;margin-bottom:4px}
.stat-value{
  font-size:28px;font-weight:700;line-height:1;color:var(--text-h);
  font-family:'Plus Jakarta Sans',sans-serif;margin-bottom:4px
}
.stat-value.red{color:#EF4444}
.stat-sub{font-size:11px;font-weight:500}
.stat-sub.up{color:#10B981}
.stat-sub.warn{color:#F59E0B}

/* 图表 */
.charts{display:flex;gap:14px}
.chart-card{flex:1;padding:14px}
.line-card{min-width:0}
.pie-card{width:220px;flex-shrink:0}
.card-title-row{display:flex;align-items:center;justify-content:space-between}
.card-title{
  font-size:14px;font-weight:600;color:var(--text-h);
  font-family:'Plus Jakarta Sans',sans-serif;display:flex;align-items:center;gap:6px
}
.cnt{font-size:12px;color:var(--text-f);font-weight:400}
.badge-red{
  background:#EF4444;color:#fff;
  font-size:10px;font-weight:700;padding:1px 6px;border-radius:10px
}

/* seg按钮 */
.seg-btns{display:flex;background:var(--bg);border-radius:var(--radius-sm);padding:2px;gap:2px}
.seg-btns button{
  background:none;border:none;outline:none;
  font-size:12px;color:var(--text-c);padding:3px 10px;
  border-radius:6px;cursor:pointer;font-family:inherit;
  transition:background var(--transition),color var(--transition),box-shadow var(--transition);
}
.seg-btns button.active{
  background:var(--surface);color:var(--text-h);font-weight:600;
  box-shadow:0 1px 3px rgba(0,0,0,0.1)
}

/* 漏斗 */
.bottom-cards{display:flex;gap:14px}
.funnel-card{flex:1;padding:14px}
.funnel{display:flex;flex-direction:column;gap:10px;margin-top:14px}
.f-step{display:flex;align-items:center;justify-content:space-between}
.f-left{display:flex;align-items:center;gap:10px;flex:1}
.f-label{font-size:13px;color:var(--text-m);width:56px;flex-shrink:0}
.f-bar-bg{width:100px;height:6px;background:#F3F4F6;border-radius:3px;overflow:hidden}
.f-bar-fill{height:100%;border-radius:3px;transition:width 0.4s ease}
.f-right{display:flex;align-items:center;gap:4px;flex-shrink:0}
.f-num{font-size:14px;font-weight:700;font-family:'Plus Jakarta Sans',sans-serif;color:var(--text-h)}
.f-pct{font-size:11px;color:var(--text-f)}

/* 超时 */
.alert-card{width:260px;flex-shrink:0;padding:14px}
.alert-list{display:flex;flex-direction:column;margin-top:10px;gap:8px}
.alert-item{display:flex;align-items:center;gap:10px}
.a-ch{font-size:18px;flex-shrink:0}
.a-info{flex:1;min-width:0}
.a-name{
  font-size:13px;font-weight:600;color:var(--text-h);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.a-pro{
  font-size:11px;color:var(--text-f);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px
}
.a-overdue{font-size:11px;color:#EF4444;font-weight:600;font-family:'Plus Jakarta Sans',sans-serif;flex-shrink:0}
.a-ok{font-size:13px;color:#10B981;text-align:center;padding:10px 0}

/* 询盘卡片 */
.inq-card{height:100%;display:flex;flex-direction:column;overflow:hidden}
.flt{display:flex;gap:8px;flex-wrap:wrap}
.fsel{
  background:var(--bg);border:1px solid var(--border);
  border-radius:var(--radius-sm);padding:4px 8px;
  font-size:12px;color:var(--text-m);font-family:inherit;
  outline:none;cursor:pointer;transition:border-color var(--transition);
}
.fsel:focus{border-color:var(--primary)}

/* 询盘列表 */
.inq-scroll{flex:1;overflow-y:auto;padding:14px 16px}
.inq-item{
  border-radius:var(--radius-sm);margin-bottom:10px;
  cursor:pointer;overflow:hidden;
  background:var(--surface);border:1px solid transparent;
  transition:background var(--transition),border-color var(--transition),box-shadow var(--transition);
}
.inq-item:hover{background:#F9FAFB;box-shadow:var(--shadow-sm)}
.inq-item.is-open{background:#F0F4FF;border-color:#BFDBFE}
.inq-item.is-danger{border-left:3px solid #EF4444}
.inq-row{display:flex;align-items:center;gap:10px;padding:10px 12px}
.inq-ch{font-size:18px;flex-shrink:0}
.inq-info{flex:1;min-width:0}
.inqname{
  font-size:13px;font-weight:600;color:var(--text-h);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.inqpro{
  font-size:11px;color:var(--text-f);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px
}
.inq-right{display:flex;flex-direction:column;align-items:flex-end;gap:3px;flex-shrink:0}
.inq-time{font-size:11px;color:var(--text-f);font-family:'DM Sans',sans-serif}
.inq-st{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px}
.st-pending{background:#FEF3C7;color:#D97706}
.st-replied{background:#D1FAE5;color:#059669}
.st-following{background:#DBEAFE;color:#2563EB}
.st-closed{background:#D1FAE5;color:#059669}
.st-invalid{background:#F3F4F6;color:#9CA3AF}

/* 展开 */
.inq-detail{padding:10px 12px 12px;border-top:1px solid var(--border)}
.det-block{margin-bottom:8px}
.det-head{font-size:11px;font-weight:600;color:var(--text-c);margin-bottom:5px}
.det-body{
  font-size:12px;color:var(--text-m);line-height:1.7;
  background:#F9FAFB;padding:9px 11px;border-radius:7px;border-left:3px solid #3B82F6
}
.det-div{height:1px;background:#F3F4F6;margin:8px 0}
.det-reply{margin-bottom:6px}
.r-meta{font-size:11px;color:var(--text-f);margin-bottom:3px;font-family:'DM Sans',sans-serif}
.r-body{
  font-size:12px;color:var(--text-m);line-height:1.7;
  background:#F0FDF4;padding:8px 11px;border-radius:7px;border-left:3px solid #22C55E
}
.det-btns{display:flex;gap:6px;margin-top:10px}
.btn{
  background:var(--surface);border:1px solid var(--border);
  border-radius:7px;padding:5px 12px;
  font-size:12px;font-family:inherit;color:var(--text-m);
  cursor:pointer;transition:background var(--transition),border-color var(--transition);
}
.btn:hover{background:#F5F6FA;border-color:#D1D5DB}
.btn-primary{
  background:var(--primary);border-color:var(--primary);color:#fff
}
.btn-primary:hover{background:var(--primary-hover)}

</style>