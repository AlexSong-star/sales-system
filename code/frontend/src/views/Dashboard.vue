<template>
  <div class="layout">

    <!-- 移动端顶部栏 -->
    <header class="mobile-header">
      <button class="hamburger" @click="drawerOpen = !drawerOpen" aria-label="打开菜单">
        <span></span><span></span><span></span>
      </button>
      <div class="mobile-logo">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        销售系统
      </div>
      <div class="mobile-avatar">白</div>
    </header>

    <!-- 遮罩 -->
    <div class="sidebar-overlay" :class="{ show: drawerOpen }" @click="drawerOpen = false"></div>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-open': drawerOpen }">
      <div class="logo">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        <span>销售系统</span>
      </div>
      <nav class="nav">
        <div class="nav-item active" @click="$router.push('/dashboard'); drawerOpen=false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span class="txt">仪表盘</span>
        </div>
        <div class="nav-item" @click="$router.push('/inquiries'); drawerOpen=false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span class="txt">询盘管理</span>
        </div>
        <div class="nav-item" @click="$router.push('/customers'); drawerOpen=false">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span class="txt">客户管理</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容 -->
    <div class="main">
      <header class="topbar desktop-topbar">
        <div class="topbar-left">
          <div class="page-title">销售仪表盘</div>
          <div class="page-sub">实时追踪三个渠道的询盘转化情况</div>
        </div>
        <div class="topbar-right">
          <div class="user-avatar">白</div>
        </div>
      </header>

      <div class="content">

        <!-- 左侧 -->
        <div class="left">
          <!-- 统计卡片 -->
          <div class="stats">
            <div class="stat" v-for="s in stats" :key="s.label">
              <div class="stat-accent" :style="{ background: s.accent }"></div>
              <div class="stat-icon" :style="{ background: s.iconBg }">
                <span v-html="s.icon"></span>
              </div>
              <div class="stat-info">
                <div class="stat-label">{{ s.label }}</div>
                <div class="stat-value" :class="s.valueClass">{{ s.value }}</div>
                <div class="stat-sub">
                  <span v-if="s.trend === 'up'" class="trend up">↑</span>
                  <span v-if="s.trend === 'down'" class="trend down">↓</span>
                  {{ s.sub }}
                </div>
              </div>
            </div>
          </div>

          <!-- 图表 -->
          <div class="charts">
            <div class="card chart-card line-card">
              <div class="card-head">
                <div class="card-title">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                  询盘趋势
                </div>
                <div class="seg-btns">
                  <button :class="{ active: trendRange === '7d' }" @click="trendRange = '7d'">7天</button>
                  <button :class="{ active: trendRange === '30d' }" @click="trendRange = '30d'">30天</button>
                </div>
              </div>
              <div ref="lineChartRef" class="chart-container"></div>
            </div>
            <div class="card chart-card pie-card">
              <div class="card-head">
                <div class="card-title">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
                  渠道分布
                </div>
              </div>
              <div ref="pieChartRef" class="chart-container"></div>
            </div>
          </div>

          <!-- 漏斗+超时 -->
          <div class="bottom-cards">
            <div class="card funnel-card">
              <div class="card-head">
                <div class="card-title">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
                  转化漏斗
                </div>
              </div>
              <div class="funnel">
                <div class="f-step" v-for="(f, i) in funnel" :key="i">
                  <div class="f-left">
                    <span class="f-label">{{ f.label }}</span>
                    <span class="f-bar-bg">
                      <span class="f-bar-fill" :style="{ width: (f.pct || 0) + '%', background: f.color }"></span>
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
              <div class="card-head">
                <div class="card-title">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#E85D4C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                  超时待处理
                </div>
                <span class="badge-red">{{ alerts.length }}</span>
              </div>
              <div class="alert-list">
                <div class="alert-item" v-for="a in alerts" :key="a.id">
                  <span class="a-ch" v-html="chIcon(a.channel)"></span>
                  <div class="a-info">
                    <div class="a-name">{{ a.customer }}</div>
                    <div class="a-pro">{{ a.product }}</div>
                  </div>
                  <div class="a-overdue">
                    <span class="overdue-dot"></span>
                    {{ a.overdue }}未回复
                  </div>
                </div>
                <div v-if="!alerts.length" class="a-ok">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  暂无超时
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：询盘列表 -->
        <div class="right">
          <div class="card inq-card">
            <div class="card-head">
              <div class="card-title">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                询盘列表
                <span class="cnt">{{ filtered.length }} 条</span>
              </div>
              <div class="flt">
                <select v-model="fChannel" class="fsel">
                  <option value="">全部渠道</option>
                  <option value="email">邮件</option>
                  <option value="whatsapp">WhatsApp</option>
                  <option value="alibaba">阿里站</option>
                </select>
                <select v-model="fStatus" class="fsel">
                  <option value="">全部状态</option>
                  <option value="pending">待回复</option>
                  <option value="replied">已回复</option>
                  <option value="following">跟进中</option>
                  <option value="closed">已成交</option>
                  <option value="invalid">无效</option>
                </select>
              </div>
            </div>
            <div class="inq-scroll">
              <div
                v-for="item in filtered"
                :key="item.id"
                class="inq-item"
                :class="{ 'is-danger': item.overHours > 24, ['ch-' + item.channel]: true }"
                @click="$router.push('/inquiry/' + item.id)"
              >
                <div class="inq-row">
                  <div class="inq-ch-wrap">
                    <span class="inq-ch" v-html="chIcon(item.channel)"></span>
                  </div>
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
              <div v-if="!filtered.length" class="empty-state">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <p>暂无询盘</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getStats, getInquiries, getTrend } from '../api'
import * as echarts from 'echarts'

const router = useRouter()
const route = useRoute()
const drawerOpen = ref(false)
const trendRange = ref('7d')
const trendData = ref([])
// searchKw removed
const fChannel = ref('')
const fStatus = ref('')
const lineChartRef = ref(null)
const pieChartRef = ref(null)

const chIcon = (c) => {
  const map = {
    email: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    whatsapp: '<svg width="18" height="18" viewBox="0 0 24 24" fill="#22C55E" stroke="none"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>',
    alibaba: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
  }
  return map[c] || '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
}
const stLabel = (s) => ({ pending:'待回复', replied:'已回复', following:'跟进中', closed:'已成交', invalid:'无效' }[s] || s)

const stats = ref([
  { label:'今日询盘', value:0, sub:'今日新增', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>', iconBg:'#EEF2FF', accent:'#4338CA', valueClass:'', subClass:'', trend:'up' },
  { label:'本周询盘', value:0, sub:'本周合计', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>', iconBg:'#ECFDF5', accent:'#10B981', valueClass:'', subClass:'', trend:'up' },
  { label:'待回复', value:0, sub:'需尽快处理', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E85D4C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>', iconBg:'#FEF2F2', accent:'#E85D4C', valueClass:'red', subClass:'warn', trend:'down' },
  { label:'本月成交', value:0, sub:'已成交', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>', iconBg:'#ECFDF5', accent:'#10B981', valueClass:'', subClass:'', trend:'up' },
])
const funnel = ref([
  { label:'收到询盘', num:0, pct:null, color:'#94A3B8' },
  { label:'已回复', num:0, pct:75, color:'#818CF8' },
  { label:'跟进中', num:0, pct:27, color:'#F59E0B' },
  { label:'已成交', num:0, pct:12, color:'#10B981' },
])
const alerts = ref([])
const inquiries = ref([
  { id:1, channel:'email', customer:'Michael Johnson', product:'Paper Cups 50,000pcs', time:'2小时前', status:'following', overHours:5 },
  { id:2, channel:'whatsapp', customer:'Emma Schmidt', product:'Custom Boxes 5,000', time:'5小时前', status:'replied', overHours:0 },
  { id:3, channel:'alibaba', customer:'Li Wei', product:'Eco Bags 10,000', time:'1天前', status:'pending', overHours:26 },
  { id:4, channel:'email', customer:'Sarah Miller', product:'Paper Napkins 20,000pcs', time:'1天前', status:'closed', overHours:0 },
  { id:5, channel:'email', customer:'Ahmed Hassan', product:'Paper Cups 30,000', time:'2天前', status:'pending', overHours:26 },
  { id:6, channel:'whatsapp', customer:'Maria Garcia', product:'Paper Straws 8,000', time:'3天前', status:'following', overHours:0 },
  { id:7, channel:'alibaba', customer:'Chen Wei', product:'Pizza Boxes 3,000', time:'4天前', status:'invalid', overHours:0 },
])
const filtered = computed(() =>
  inquiries.value.filter(i => {
    if (fChannel.value && i.channel !== fChannel.value) return false
    if (fStatus.value && i.status !== fStatus.value) return false
    return true
  })
)
const alertCount = computed(() => alerts.value.length)
let lineChart = null, pieChart = null

onMounted(async () => {
  try {
    const [statsData, inqData, trendDataResult] = await Promise.all([getStats(), getInquiries(), getTrend(trendRange.value === '7d' ? 7 : 30)])
    trendData.value = trendDataResult
    stats.value = [
      { label:'今日询盘', value:statsData.today_inquiries, sub:'今日新增', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4338CA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>', iconBg:'#EEF2FF', accent:'#4338CA', valueClass:'', subClass:'', trend:'up' },
      { label:'本周询盘', value:statsData.week_inquiries, sub:'本周合计', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>', iconBg:'#ECFDF5', accent:'#10B981', valueClass:'', subClass:'', trend:'up' },
      { label:'待回复', value:statsData.pending, sub:'需尽快处理', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E85D4C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>', iconBg:'#FEF2F2', accent:'#E85D4C', valueClass: statsData.pending > 0 ? 'red' : '', subClass: statsData.pending > 0 ? 'warn' : '', trend: statsData.pending > 0 ? 'down' : 'up' },
      { label:'本月成交', value:statsData.closed, sub:'已成交', icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>', iconBg:'#ECFDF5', accent:'#10B981', valueClass:'', subClass:'', trend:'up' },
    ]
    inquiries.value = inqData.map(i => ({
      ...i,
      time: new Date(i.created_at).toLocaleString('zh-CN', { month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' }),
      overHours: Math.floor((Date.now() - new Date(i.created_at)) / 3600000),
    }))
    const total = inqData.length || 1
    funnel.value[0].num = inqData.length
    funnel.value[0].pct = 100
    funnel.value[1].num = inqData.filter(i => ['replied','following','closed'].includes(i.status)).length
    funnel.value[1].pct = Math.round(funnel.value[1].num / total * 100)
    funnel.value[2].num = inqData.filter(i => i.status === 'following').length
    funnel.value[2].pct = Math.round(funnel.value[2].num / total * 100)
    funnel.value[3].num = inqData.filter(i => i.status === 'closed').length
    funnel.value[3].pct = Math.round(funnel.value[3].num / total * 100)
    alerts.value = inqData.filter(i => i.status === 'pending' && Math.floor((Date.now() - new Date(i.created_at)) / 3600000) > 24).slice(0, 5)

    if (lineChartRef.value) {
      lineChart = echarts.init(lineChartRef.value)
      lineChart.setOption({
        tooltip:{ trigger:'axis', backgroundColor:'#1F2937', borderColor:'#374151', textStyle:{ color:'#F9FAFB', fontSize:12 }, axisPointer:{ type:'cross', label:{ backgroundColor:'#1F2937' } } },
        legend:{ data:['邮件','WhatsApp','阿里站'], bottom:0, textStyle:{ fontSize:11, color:'#6B7280' }, icon:'circle', itemWidth:8 },
        grid:{ top:8, bottom:36, left:36, right:12 },
        xAxis:{ type:'category', data: trendData.value.map(p => p.date), axisLine:{ lineStyle:{ color:'#E8E9F0' } }, axisLabel:{ fontSize:11, color:'#9CA3AF' }, splitLine:{ show:false } },
        yAxis:{ type:'value', splitLine:{ lineStyle:{ color:'#F3F4F6', type:'dashed' } }, axisLine:{ show:false }, axisTick:{ show:false }, axisLabel:{ fontSize:11, color:'#9CA3AF' } },
        series:[
          { name:'邮件', type:'line', smooth:true, data: trendData.value.map(p => p.email), symbol:'circle', symbolSize:6, lineStyle:{ color:'#4338CA', width:2.5 }, itemStyle:{ color:'#4338CA', borderWidth:2, borderColor:'#fff' }, areaStyle:{ color:{ type:'linear', x:0, y:0, x2:0, y2:1, colorStops:[{ offset:0, color:'rgba(67,56,202,0.12)' },{ offset:1, color:'rgba(67,56,202,0)' }] }, origin:'start' } },
          { name:'WhatsApp', type:'line', smooth:true, data: trendData.value.map(p => p.whatsapp), symbol:'circle', symbolSize:6, lineStyle:{ color:'#10B981', width:2.5 }, itemStyle:{ color:'#10B981', borderWidth:2, borderColor:'#fff' }, areaStyle:{ color:{ type:'linear', x:0, y:0, x2:0, y2:1, colorStops:[{ offset:0, color:'rgba(16,185,129,0.10)' },{ offset:1, color:'rgba(16,185,129,0)' }] }, origin:'start' } },
          { name:'阿里站', type:'line', smooth:true, data: trendData.value.map(p => p.alibaba), symbol:'circle', symbolSize:6, lineStyle:{ color:'#F97316', width:2.5 }, itemStyle:{ color:'#F97316', borderWidth:2, borderColor:'#fff' }, areaStyle:{ color:{ type:'linear', x:0, y:0, x2:0, y2:1, colorStops:[{ offset:0, color:'rgba(249,115,22,0.10)' },{ offset:1, color:'rgba(249,115,22,0)' }] }, origin:'start' } },
        ]
      })
    }
    if (pieChartRef.value) {
      const pieTotal = statsData.email_count + statsData.whatsapp_count + statsData.alibaba_count || 1
      pieChart = echarts.init(pieChartRef.value)
      pieChart.setOption({
        tooltip:{ trigger:'item', backgroundColor:'#1F2937', borderColor:'#374151', textStyle:{ color:'#F9FAFB', fontSize:12 } },
        legend:{ orient:'vertical', right:8, top:16, textStyle:{ fontSize:11, color:'#6B7280' } },
        series:[{ type:'pie', radius:['55%','80%'], center:['38%','50%'], label:{ show:false },
          data:[
            { value:statsData.email_count || 0, name:'邮件', itemStyle:{ color:'#4338CA' } },
            { value:statsData.whatsapp_count || 0, name:'WhatsApp', itemStyle:{ color:'#10B981' } },
            { value:statsData.alibaba_count || 0, name:'阿里站', itemStyle:{ color:'#F97316' } },
          ] }]
      })
    }
  } catch (e) { console.error('API加载失败:', e) }

  const handleResize = () => { lineChart?.resize(); pieChart?.resize() }
  window.addEventListener('resize', handleResize)
  onUnmounted(() => { window.removeEventListener('resize', handleResize); lineChart?.dispose(); pieChart?.dispose() })
})

watch(trendRange, async (val) => {
  trendData.value = await getTrend(val === '7d' ? 7 : 30)
  if (lineChart) {
    lineChart.setOption({
      xAxis:{ data: trendData.value.map(p => p.date) },
      series:[
        { data: trendData.value.map(p => p.email) },
        { data: trendData.value.map(p => p.whatsapp) },
        { data: trendData.value.map(p => p.alibaba) },
      ]
    })
  }
})
</script>

<style scoped>
/* ===== CSS Variables ===== */
:root {
  --bg: #F8F9FC;
  --surface: #FFFFFF;
  --border: #E8E9F0;
  --border-strong: #D1D5DB;
  --text-h: #111827;
  --text-m: #374151;
  --text-c: #6B7280;
  --text-f: #9CA3AF;
  --primary: #4338CA;
  --primary-light: #6366F1;
  --primary-bg: #EEF2FF;
  --primary-hover: #3730A3;
  --danger: #E85D4C;
  --danger-bg: #FEF2F2;
  --success: #10B981;
  --success-bg: #ECFDF5;
  --warning: #F59E0B;
  --warning-bg: #FFFBEB;
  --sidebar-bg: #FFFFFF;
  --sidebar-text: #323639;
  --sidebar-text-active: #006BE6;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.14);
  --radius: 10px;
  --radius-sm: 6px;
  --radius-lg: 14px;
  --transition: 0.18s ease;
  --sidebar-w: 200px;
}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body,#app{height:100%;overflow:hidden}
body{font-family:'DM Sans','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text-h);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px;border-radius:4px}

/* ========== 整体布局 ========== */
.layout{display:flex;height:100vh;overflow:hidden;width:100vw}

/* ========== 移动端顶栏 ========== */
.mobile-header{
  display:none;position:fixed;top:0;left:0;right:0;z-index:200;
  height:56px;background:var(--surface);border-bottom:1px solid var(--border);
  padding:0 16px;align-items:center;justify-content:space-between;
  box-shadow:var(--shadow-sm);
}
.mobile-logo{
  display:flex;align-items:center;gap:7px;
  font-size:14px;font-weight:700;font-family:'Plus Jakarta Sans',sans-serif;color:var(--text-h);
}
.mobile-avatar{width:32px;height:32px;background:var(--primary);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:12px}
.hamburger{width:36px;height:36px;background:none;border:none;cursor:pointer;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:5px;padding:4px;border-radius:6px}
.hamburger:hover{background:#F3F4F6}
.hamburger span{display:block;width:20px;height:2px;background:#374151;border-radius:2px}

/* ========== 遮罩 ========== */
.sidebar-overlay{display:none;position:fixed;inset:0;z-index:299;background:rgba(0,0,0,0.5);opacity:0;transition:opacity var(--transition)}
.sidebar-overlay.show{display:block;opacity:1}

/* ========== 侧边栏 ========== */
.sidebar{
  width:200px;background:var(--sidebar-bg);
  display:flex;flex-direction:column;flex-shrink:0;
  transition:transform var(--transition);z-index:300;
}
.logo{
  display:flex;align-items:center;gap:10px;
  padding:0 20px;height:64px;
  border-bottom:1px solid rgba(0,0,0,0.06);
  color:#000;font-size:18px;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
}
.logo span{font-size:20px;font-weight:700}
.nav{display:flex;flex-direction:column;padding:12px 0;gap:1px}
.nav-item{
  display:flex;align-items:center;
  padding:10px 20px;cursor:pointer;
  color:var(--sidebar-text);font-size:13px;gap:10px;
  transition:background var(--transition),color var(--transition);
  text-decoration:none;
  box-sizing:border-box;
}
.nav-item:hover{color:var(--sidebar-text-active);background:#006BE610}
.nav-item.active{
  color:var(--sidebar-text-active);
  background:#006BE626;
  border-left:3px solid #006BE6;
  padding:10px 20px 10px 17px;
  box-sizing:border-box;
}
.nav-item.disabled{opacity:0.4;cursor:not-allowed;pointer-events:none}
.icon{font-size:16px;flex-shrink:0}

/* ========== 主区 ========== */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* ========== 桌面端顶栏 ========== */
.topbar{
  height:64px;background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;flex-shrink:0;
}
.topbar-left{display:flex;flex-direction:column;justify-content:center}
.page-title{font-size:20px;font-weight:700}
.page-sub{font-size:14px;color:var(--text-f);margin-top:2px}
.topbar-right{display:flex;align-items:center;gap:16px}
.search-bar{
  display:flex;align-items:center;gap:8px;
  background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:7px 12px;
  transition:border-color var(--transition),box-shadow var(--transition);
}
.search-bar:focus-within{border-color:var(--primary);box-shadow:0 0 0 3px rgba(67,56,202,0.08)}
.search-bar input{background:none;border:none;outline:none;font-size:13px;color:var(--text-m);width:200px;font-family:inherit}
.search-bar input::placeholder{color:var(--text-f)}
.user-avatar{
  width:36px;height:36px;background:var(--primary);color:#fff;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;
  font-family:'Plus Jakarta Sans',sans-serif;cursor:pointer;
  transition:opacity var(--transition),transform var(--transition);
}
.user-avatar:hover{opacity:0.85;transform:scale(1.05)}

/* ========== 内容区 ========== */
.content{display:flex;flex:1;overflow:hidden;gap:18px;padding:20px}
.left{flex:1;display:flex;flex-direction:column;gap:18px;overflow-y:auto;min-width:0}
.right{width:380px;flex-shrink:0;overflow:hidden;display:flex;flex-direction:column}

/* ========== 卡片通用 ========== */
.card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);
  transition:box-shadow var(--transition),transform var(--transition);
}
.card:hover{box-shadow:var(--shadow-md);transform:translateY(-1px)}
.card-head{
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:10px;
  padding:18px 18px 0;
}
.card-title{
  font-size:14px;font-weight:700;color:var(--text-h);
  font-family:'Plus Jakarta Sans',sans-serif;
  display:flex;align-items:center;gap:7px;
}
.cnt{font-size:12px;color:var(--text-f);font-weight:400}
.badge-red{
  background:var(--danger);color:#fff;
  font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px;
}
.seg-btns{display:flex;background:var(--bg);border-radius:var(--radius-sm);padding:2px;gap:2px}
.seg-btns button{
  background:none;border:none;outline:none;
  font-size:12px;color:var(--text-c);padding:4px 12px;border-radius:5px;
  cursor:pointer;font-family:inherit;
  transition:background var(--transition),color var(--transition),box-shadow var(--transition);
}
.seg-btns button.active{
  background:var(--surface);color:var(--text-h);font-weight:600;
  box-shadow:0 1px 4px rgba(0,0,0,0.1);
}

/* ========== 统计卡片 ========== */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.stat{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:0;overflow:hidden;
  display:flex;align-items:center;gap:0;
  transition:box-shadow var(--transition),transform var(--transition),border-color var(--transition);
}
.stat:hover{box-shadow:var(--shadow-md);transform:translateY(-2px);border-color:#D1D5DB}
.stat-accent{width:4px;align-self:stretch;flex-shrink:0}
.stat-icon{
  width:48px;height:48px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin:16px 0 16px 14px;
}
.stat-info{flex:1;min-width:0;padding:16px 14px 16px 12px}
.stat-label{font-size:12px;color:var(--text-c);font-weight:500;margin-bottom:5px}
.stat-value{
  font-size:28px;font-weight:800;line-height:1;
  color:var(--text-h);font-family:'Plus Jakarta Sans',sans-serif;margin-bottom:5px;
  letter-spacing:-0.5px;
}
.stat-value.red{color:var(--danger)}
.stat-sub{
  font-size:11px;font-weight:500;color:var(--text-f);
  display:flex;align-items:center;gap:4px;
}
.trend{font-size:12px;font-weight:700}
.trend.up{color:var(--success)}
.trend.down{color:var(--danger)}
.stat-sub.up{color:var(--success)}
.stat-sub.warn{color:var(--warning)}

/* ========== 图表 ========== */
.charts{display:flex;gap:16px}
.chart-card{flex:1;padding:18px;min-width:0;display:flex;flex-direction:column}
.chart-container{height:200px;margin-top:16px;min-height:0}
.pie-card{width:240px;flex-shrink:0}

/* ========== 漏斗 ========== */
.bottom-cards{display:flex;gap:16px}
.funnel-card{flex:1;padding:18px}
.funnel{display:flex;flex-direction:column;gap:12px;margin-top:16px}
.f-step{display:flex;align-items:center;justify-content:space-between}
.f-left{display:flex;align-items:center;gap:12px;flex:1}
.f-label{font-size:13px;color:var(--text-m);width:60px;flex-shrink:0;font-weight:500}
.f-bar-bg{width:120px;height:6px;background:#F3F4F6;border-radius:3px;overflow:hidden;flex-shrink:0}
.f-bar-fill{height:100%;border-radius:3px;transition:width 0.5s cubic-bezier(0.4,0,0.2,1)}
.f-right{display:flex;align-items:center;gap:5px;flex-shrink:0}
.f-num{font-size:15px;font-weight:800;color:var(--text-h);font-family:'Plus Jakarta Sans',sans-serif}
.f-pct{font-size:11px;color:var(--text-f)}

/* ========== 超时告警 ========== */
.alert-card{width:270px;flex-shrink:0;padding:18px}
.alert-list{display:flex;flex-direction:column;margin-top:14px;gap:10px}
.alert-item{display:flex;align-items:center;gap:10px}
.a-ch{font-size:18px;flex-shrink:0}
.a-info{flex:1;min-width:0}
.a-name{font-size:13px;font-weight:600;color:var(--text-h);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.a-pro{font-size:11px;color:var(--text-f);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px}
.a-overdue{
  font-size:11px;color:var(--danger);font-weight:600;
  font-family:'Plus Jakarta Sans',sans-serif;flex-shrink:0;
  display:flex;align-items:center;gap:5px;
}
.overdue-dot{
  width:6px;height:6px;background:var(--danger);
  border-radius:50%;flex-shrink:0;animation:pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.a-ok{
  display:flex;align-items:center;justify-content:center;gap:7px;
  font-size:13px;color:var(--success);padding:8px 0;
}

/* ========== 询盘列表 ========== */
.inq-card{height:100%;display:flex;flex-direction:column;overflow:hidden}
.flt{display:flex;gap:8px;flex-wrap:wrap}
.fsel{
  background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:5px 10px;font-size:12px;color:var(--text-m);
  font-family:inherit;outline:none;cursor:pointer;
  transition:border-color var(--transition);
}
.fsel:focus{border-color:var(--primary)}
.inq-scroll{flex:1;overflow-y:auto;padding:14px 16px}
.inq-item{
  border-radius:var(--radius-sm);margin-bottom:8px;cursor:pointer;
  overflow:hidden;background:var(--surface);
  border:1px solid var(--border);
  transition:border-color var(--transition),box-shadow var(--transition),transform var(--transition);
}
.inq-item:hover{
  border-color:var(--primary);box-shadow:var(--shadow-sm);transform:translateY(-1px);
}
.inq-item.is-danger{border-left:3px solid var(--danger) !important}
.inq-item.ch-email:hover{border-left-color:#3B82F6}
.inq-item.ch-whatsapp:hover{border-left-color:#22C55E}
.inq-item.ch-alibaba:hover{border-left-color:#F97316}
.inq-row{display:flex;align-items:center;gap:12px;padding:11px 13px}
.inq-ch-wrap{
  width:34px;height:34px;background:var(--bg);border-radius:8px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.inq-ch{display:flex;align-items:center;justify-content:center}
.inq-info{flex:1;min-width:0}
.inqname{font-size:13px;font-weight:600;color:var(--text-h);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.inqpro{font-size:11px;color:var(--text-f);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.inq-right{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0}
.inq-time{font-size:11px;color:var(--text-f);font-family:'DM Sans',sans-serif}
.inq-st{font-size:11px;font-weight:600;padding:2px 9px;border-radius:20px}
.st-pending{background:var(--warning-bg);color:#B45309}
.st-replied{background:var(--success-bg);color:#065F46}
.st-following{background:var(--primary-bg);color:var(--primary)}
.st-closed{background:var(--success-bg);color:#065F46}
.st-invalid{background:#F9FAFB;color:#9CA3AF}

.empty-state{
  text-align:center;padding:40px 20px;
  display:flex;flex-direction:column;align-items:center;gap:10px;
}
.empty-state p{font-size:13px;color:var(--text-f);margin:0}

/* =============================================
   移动端适配 — 断点 768px
   ============================================= */
@media (max-width: 768px) {
  .mobile-header { display: flex; }
  .desktop-topbar { display: none; }

  .sidebar {
    position: fixed;top: 0;left: 0;bottom: 0;z-index: 300;
    transform: translateX(-100%);width: 240px;
    box-shadow: var(--shadow-lg);
  }
  .sidebar.sidebar-open { transform: translateX(0); }
  .sidebar{background:#FFFFFF!important;box-shadow:2px 0 20px rgba(0,0,0,0.15)!important}
  .sidebar .logo{color:#111827!important;border-bottom-color:#E8E9F0!important}
  .sidebar .logo span{color:#374151!important}
  .nav-item{color:#374151!important}
  .nav-item:hover{color:var(--primary)!important;background:var(--primary-bg)!important}
  .nav-item.active{color:var(--primary)!important;background:var(--primary-bg)!important;border-left-color:var(--primary)!important}
  .nav-item.disabled{color:#9CA3AF!important}

  .main{padding-top:56px}

  .content{flex-direction:column;overflow-y:auto;gap:14px;padding:14px}
  .left{overflow:visible}
  .right{width:100%;flex-shrink:0;max-height:440px}

  .stats{grid-template-columns:repeat(2,1fr);gap:12px}
  .stat{flex-direction:row;gap:0}
  .stat-icon{margin:14px 0 14px 12px}
  .stat-info{padding:14px 12px}
  .stat-value{font-size:24px}

  .charts{flex-direction:column;gap:12px}
  .chart-card{width:100%!important}
  .pie-card{display:none}

  .bottom-cards{flex-direction:column}
  .alert-card{width:100%}

  .topbar-right .search-bar{display:none}
}

@media (max-width: 480px) {
  .stats{grid-template-columns:repeat(2,1fr);gap:10px}
  .stat{flex-direction:column;align-items:flex-start;gap:0;padding-bottom:12px}
  .stat-icon{margin:14px 0 4px 12px}
  .stat-info{padding:0 12px 12px}
  .stat-value{font-size:22px}
  .f-bar-bg{width:80px}
}

</style>
