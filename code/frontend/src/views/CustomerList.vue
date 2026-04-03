<template>
  <div class="layout">

    <!-- 移动端顶栏 -->
    <header class="mobile-header" style="display:none">
      <button class="hamburger" @click="drawerOpen = !drawerOpen" aria-label="打开菜单">
        <span></span><span></span><span></span>
      </button>
      <div class="mobile-logo">👥 客户管理</div>
      <div class="mobile-user">白</div>
    </header>

    <!-- 遮罩 -->
    <div class="sidebar-overlay" :class="{ show: drawerOpen }" @click="drawerOpen = false"></div>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-open': drawerOpen }">
      <div class="logo">📊 <span>销售系统</span></div>
      <nav class="nav">
        <div class="nav-item" @click="$router.push('/dashboard')">
          <span class="icon">📊</span><span class="txt">仪表盘</span>
        </div>
        <div class="nav-item" @click="$router.push('/inquiries')">
          <span class="icon">📋</span><span class="txt">询盘管理</span>
        </div>
        <div class="nav-item active">
          <span class="icon">👥</span><span class="txt">客户管理</span>
        </div>
        <div class="nav-item" @click="$router.push('/orders')">
          <span class="icon">📦</span><span class="txt">订单管理</span>
        </div>
        <div class="nav-item" @click="$router.push('/settings')">
          <span class="icon">⚙️</span><span class="txt">系统设置</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容 -->
    <div class="main">

      <!-- 顶栏 -->
      <header class="topbar">
        <div class="topbar-left">
          <div class="page-title">客户管理</div>
          <div class="page-sub">共 {{ customers.length }} 位客户</div>
        </div>
        <div class="topbar-right">
          <div class="search-bar">
            <span class="search-icon">🔍</span>
            <input placeholder="搜索客户姓名、公司..." v-model="searchKw" />
          </div>
          <div class="user-avatar">白</div>
        </div>
      </header>

      <!-- 主体 -->
      <div class="content">

        <!-- 左侧：客户列表 -->
        <div class="left">
          <!-- 筛选栏 -->
          <div class="filter-bar">
            <div class="filter-group">
              <label>等级</label>
              <select v-model="fLevel" class="fsel">
                <option value="">全部</option>
                <option value="A">🅰️ A级（高意向）</option>
                <option value="B">🅱️ B级（跟进中）</option>
                <option value="C">🔵 C级（潜力）</option>
              </select>
            </div>
            <div class="filter-group">
              <label>状态</label>
              <select v-model="fStatus" class="fsel">
                <option value="">全部</option>
                <option value="following">🔄 跟进中</option>
                <option value="closed">✅ 已成交</option>
                <option value="pending">⏳ 待回复</option>
                <option value="lost">❌ 已流失</option>
              </select>
            </div>
            <div class="filter-group">
              <label>来源</label>
              <select v-model="fSource" class="fsel">
                <option value="">全部渠道</option>
                <option value="email">📧 邮件</option>
                <option value="whatsapp">💬 WhatsApp</option>
                <option value="alibaba">🛒 阿里站</option>
              </select>
            </div>
          </div>

          <!-- 客户卡片列表 -->
          <div class="customer-list">
            <div
              v-for="c in filtered"
              :key="c.id"
              class="customer-card"
              :class="{ active: selectedId === c.id }"
              @click="selectCustomer(c.id)"
            >
              <div class="c-top">
                <div class="c-avatar" :class="'lv-' + c.level">{{ c.name.charAt(0) }}</div>
                <div class="c-info">
                  <div class="c-name">{{ c.name }}</div>
                  <div class="c-company">{{ c.company }}</div>
                </div>
                <div class="c-level" :class="'level-' + c.level">{{ c.level }}</div>
              </div>
              <div class="c-bottom">
                <div class="c-meta">
                  <span class="c-flag">{{ c.country }}</span>
                  <span class="c-inq-count">📋 {{ c.inquiryCount }} 次询盘</span>
                </div>
                <div class="c-status" :class="'st-' + c.status">{{ stLabel(c.status) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：客户详情 -->
        <div class="right" v-if="selected">

          <!-- 基本信息 -->
          <div class="card info-card">
            <div class="card-title">👤 客户信息</div>
            <div class="info-grid">
              <div class="info-row">
                <span class="info-label">客户ID</span>
                <span class="info-val id">{{ selected.id }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">客户姓名</span>
                <span class="info-val">{{ selected.name }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">公司名称</span>
                <span class="info-val">{{ selected.company }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">邮箱</span>
                <span class="info-val link">{{ selected.email }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">国家/城市</span>
                <span class="info-val">{{ selected.country }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">客户等级</span>
                <span class="info-val">
                  <span class="level-badge" :class="'level-' + selected.level">{{ levelLabel(selected.level) }}</span>
                </span>
              </div>
              <div class="info-row">
                <span class="info-label">创建时间</span>
                <span class="info-val">{{ selected.createdAt }}</span>
              </div>
            </div>
          </div>

          <!-- 跟进策略 -->
          <div class="card strategy-card">
            <div class="card-title">🎯 跟进策略</div>
            <div class="strategy-body">
              <div class="str-priority" :class="'prio-' + selected.priority">
                {{ prioLabel(selected.priority) }}
              </div>
              <div class="str-content">
                <div class="str-next">
                  <span class="str-label">下一步</span>
                  <span class="str-val">{{ selected.nextStep }}</span>
                </div>
                <div class="str-expected">
                  <span class="str-label">预计成交</span>
                  <span class="str-val">{{ selected.expectedClose }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 询盘记录 -->
          <div class="card inquiries-card">
            <div class="card-title">📋 询盘记录 <span class="cnt">{{ selected.inquiries.length }} 次</span></div>
            <div class="inq-list">
              <div
                class="inq-entry"
                v-for="(inq, i) in selected.inquiries"
                :key="i"
                @click="$router.push('/inquiry/' + inq.id)"
              >
                <div class="ie-top">
                  <span class="ie-product">{{ inq.product }}</span>
                  <span class="ie-intent" :class="'intent-' + inq.intent">{{ intentLabel(inq.intent) }}</span>
                </div>
                <div class="ie-meta">
                  <span class="ie-date">{{ inq.date }}</span>
                  <span class="ie-qty" v-if="inq.quantity">{{ inq.quantity }}</span>
                  <span class="ie-status" :class="'st-' + inq.status">{{ stLabel(inq.status) }}</span>
                </div>
                <div class="ie-summary" v-if="inq.summary">{{ inq.summary }}</div>
                <div class="ie-action">查看详情 →</div>
              </div>
            </div>
          </div>

        </div>

        <!-- 无选中状态 -->
        <div class="right empty-right" v-else>
          <div class="empty-state">
            <div class="empty-icon">👆</div>
            <div class="empty-text">点击左侧客户卡片<br>查看详情</div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const drawerOpen = ref(false)
const searchKw = ref('')
const fLevel = ref('')
const fStatus = ref('')
const fSource = ref('')
const selectedId = ref(null)

// Mock 数据（与吕秀才客户体系完全兼容）
const customers = ref([
  {
    id: 'C001', name: 'Michael Johnson', company: 'Pacific Trading Co.',
    email: 'michael.j@pacific-trading.com', country: '🇺🇸 USA, Los Angeles',
    level: 'A', status: 'following', source: 'email',
    createdAt: '2026-03-30', priority: 'high',
    nextStep: '等待客户确认规格后发正式报价单', expectedClose: '1-2周',
    inquiryCount: 1,
    inquiries: [
      { id: 1, product: 'Paper Cups 50,000pcs', quantity: '50,000 pcs', date: '2026-03-30',
        intent: 'high', status: 'following',
        summary: '12oz food-grade, custom logo, FOB报价已发，等待确认规格' }
    ]
  },
  {
    id: 'C002', name: 'Emma Schmidt', company: 'Euro Retail GmbH',
    email: 'e.schmidt@euroretail.de', country: '🇩🇪 Germany, Berlin',
    level: 'B', status: 'replied', source: 'whatsapp',
    createdAt: '2026-03-28', priority: 'medium',
    nextStep: '发送产品目录和报价单', expectedClose: '2-3周',
    inquiryCount: 2,
    inquiries: [
      { id: 2, product: 'Custom Boxes 5,000', quantity: '5,000 units', date: '2026-03-28',
        intent: 'medium', status: 'replied', summary: '定制彩盒，报价已发送' },
      { id: 6, product: 'Paper Straws 8,000', quantity: '8,000 pcs', date: '2026-03-29',
        intent: 'medium', status: 'following', summary: '纸吸管，混合颜色，样品已安排' }
    ]
  },
  {
    id: 'C003', name: 'Li Wei', company: 'Green Pack Asia',
    email: 'liwei@greenpack.asia', country: '🇨🇳 China, Shanghai',
    level: 'B', status: 'pending', source: 'alibaba',
    createdAt: '2026-03-27', priority: 'high',
    nextStep: '提供环保袋样品和认证资料', expectedClose: '1个月',
    inquiryCount: 1,
    inquiries: [
      { id: 3, product: 'Eco Bags 10,000', quantity: '10,000 pcs', date: '2026-03-27',
        intent: 'high', status: 'pending', summary: '生物降解袋，需求紧急' }
    ]
  },
  {
    id: 'C004', name: 'Sarah Miller', company: 'Sunrise Hospitality',
    email: 's.miller@sunrise-hosp.com', country: '🇺🇸 USA, Miami',
    level: 'A', status: 'closed', source: 'email',
    createdAt: '2026-03-20', priority: 'closed',
    nextStep: '已成交，交付中', expectedClose: '已成交',
    inquiryCount: 1,
    inquiries: [
      { id: 4, product: 'Paper Napkins 20,000pcs', quantity: '20,000 pcs', date: '2026-03-20',
        intent: 'high', status: 'closed', summary: '纸餐巾，已下单，30%定金已收' }
    ]
  },
  {
    id: 'C005', name: 'Ahmed Hassan', company: 'Dubai Hotel Group',
    email: 'ahmed.h@dubaihg.com', country: '🇦🇪 UAE, Dubai',
    level: 'C', status: 'pending', source: 'email',
    createdAt: '2026-03-25', priority: 'low',
    nextStep: '等待客户回复', expectedClose: '待定',
    inquiryCount: 1,
    inquiries: [
      { id: 5, product: 'Paper Cups 30,000', quantity: '30,000 pcs', date: '2026-03-25',
        intent: 'medium', status: 'pending', summary: '酒店用纸杯，迪拜当地有竞争供应商' }
    ]
  },
  {
    id: 'C006', name: 'Maria Garcia', company: 'Restaurante Sol',
    email: 'maria@sol-restaurante.es', country: '🇪🇸 Spain, Barcelona',
    level: 'C', status: 'following', source: 'whatsapp',
    createdAt: '2026-03-22', priority: 'low',
    nextStep: '发送纸质吸管样品册', expectedClose: '1个月+',
    inquiryCount: 1,
    inquiries: [
      { id: 6, product: 'Paper Straws 8,000', quantity: '8,000 pcs', date: '2026-03-22',
        intent: 'low', status: 'following', summary: '餐厅纸吸管，小批量试单' }
    ]
  },
])

const filtered = computed(() =>
  customers.value.filter(c => {
    if (fLevel.value && c.level !== fLevel.value) return false
    if (fStatus.value && c.status !== fStatus.value) return false
    if (fSource.value && c.source !== fSource.value) return false
    if (searchKw.value) {
      const kw = searchKw.value.toLowerCase()
      if (!c.name.toLowerCase().includes(kw) && !c.company.toLowerCase().includes(kw)) return false
    }
    return true
  })
)

const selected = computed(() =>
  selectedId.value ? customers.value.find(c => c.id === selectedId.value) : null
)

const selectCustomer = (id) => { selectedId.value = id }

const levelLabel = (l) => ({ A:'🅰️ A级（高意向）', B:'🅱️ B级（跟进中）', C:'🔵 C级（潜力）' }[l] || l)
const stLabel = (s) => ({ pending:'⏳ 待回复', replied:'✅ 已回复', following:'🔄 跟进中', closed:'🏁 已成交', lost:'❌ 已流失' }[s] || s)
const prioLabel = (p) => ({ high:'🔴 高优先级', medium:'🟡 中优先级', low:'⚪ 低优先级', closed:'✅ 已成交' }[p] || p)
const intentLabel = (i) => ({ high:'🔥 高意向', medium:'🌱 首次合作', low:'📋 普通' }[i] || i)
</script>

<style scoped>
:root {
  --bg: #F4F5F8; --surface: #FFFFFF; --border: #E5E7EB;
  --text-h: #111827; --text-m: #374151; --text-c: #6B7280; --text-f: #9CA3AF;
  --primary: #2563EB; --primary-hover: #1D4ED8;
  --sidebar-bg: #1E293B; --sidebar-text: rgba(255,255,255,0.55);
  --sidebar-text-active: #FFFFFF;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 2px 12px rgba(0,0,0,0.08);
  --radius: 12px; --radius-sm: 8px; --transition: 0.15s ease;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body,#app{height:100%;overflow:hidden}
body{font-family:'DM Sans','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text-h);font-size:14px;-webkit-font-smoothing:antialiased}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px;border-radius:4px}
:focus:not(:focus-visible){outline:none}

.layout{display:flex;height:100vh;overflow:hidden;width:100vw;max-width:100vw}

.sidebar{width:180px;background:var(--sidebar-bg);display:flex;flex-direction:column;flex-shrink:0}
.logo{display:flex;align-items:center;gap:10px;padding:0 20px;height:64px;border-bottom:1px solid rgba(255,255,255,0.06);color:#fff;font-size:18px;font-family:'Plus Jakarta Sans',sans-serif;font-weight:700}
.logo span{font-size:13px;font-weight:700}
.nav{display:flex;flex-direction:column;padding:12px 0;gap:2px}
.nav-item{display:flex;align-items:center;padding:10px 20px;cursor:pointer;color:var(--sidebar-text);font-size:13px;gap:10px;transition:background var(--transition),color var(--transition)}
.nav-item:hover{color:var(--sidebar-text-active);background:rgba(255,255,255,0.06)}
.nav-item.active{color:var(--sidebar-text-active);background:rgba(37,99,235,0.55)}
.icon{font-size:16px;flex-shrink:0}

.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

.topbar{height:64px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 20px;flex-shrink:0}
.topbar-left{display:flex;flex-direction:column;justify-content:center}
.page-title{font-size:18px;font-weight:700;color:var(--text-h);font-family:'Plus Jakarta Sans',sans-serif}
.page-sub{font-size:12px;color:var(--text-f);margin-top:1px}
.topbar-right{display:flex;align-items:center;gap:16px}
.search-bar{display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:7px 12px}
.search-bar:focus-within{border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,0.1)}
.search-bar input{background:none;border:none;outline:none;font-size:13px;color:var(--text-m);width:200px;font-family:inherit}
.search-bar input::placeholder{color:var(--text-f)}
.user-avatar{width:36px;height:36px;background:var(--primary);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;font-family:'Plus Jakarta Sans',sans-serif;cursor:pointer}

.content{display:flex;flex:1;overflow:hidden;gap:14px;padding:14px 16px 16px}

.left{flex:1;display:flex;flex-direction:column;gap:12px;overflow:hidden;min-width:0}
.right{flex-shrink:0;width:380px;overflow-y:auto;display:flex;flex-direction:column;gap:12px}
.empty-right{display:flex;align-items:center;justify-content:center}
.empty-state{text-align:center;padding:40px}
.empty-icon{font-size:40px;margin-bottom:12px}
.empty-text{font-size:13px;color:var(--text-f);line-height:1.7}

.filter-bar{display:flex;gap:12px;flex-wrap:wrap}
.filter-group{display:flex;align-items:center;gap:6px}
.filter-group label{font-size:12px;color:var(--text-f);white-space:nowrap}
.fsel{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:5px 10px;font-size:12px;color:var(--text-m);font-family:inherit;outline:none;cursor:pointer;transition:border-color var(--transition)}
.fsel:focus{border-color:var(--primary)}

.customer-list{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:8px}
.customer-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:14px;cursor:pointer;
  transition:border-color var(--transition),box-shadow var(--transition),transform var(--transition);
}
.customer-card:hover{box-shadow:var(--shadow-sm);transform:translateY(-1px)}
.customer-card.active{border-color:#BFDBFE;background:#F0F4FF}
.c-top{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.c-avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#fff;flex-shrink:0}
.lv-A{background:#DC2626}
.lv-B{background:#2563EB}
.lv-C{background:#6B7280}
.c-info{flex:1;min-width:0}
.c-name{font-size:14px;font-weight:600;color:var(--text-h);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.c-company{font-size:11px;color:var(--text-f);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px}
.c-level{font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;flex-shrink:0}
.level-A{background:#FEE2E2;color:#DC2626}
.level-B{background:#DBEAFE;color:#2563EB}
.level-C{background:#F3F4F6;color:#6B7280}
.c-bottom{display:flex;align-items:center;justify-content:space-between}
.c-meta{display:flex;align-items:center;gap:8px}
.c-flag{font-size:12px}
.c-inq-count{font-size:11px;color:var(--text-f)}
.c-status{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px}
.st-pending{background:#FEF3C7;color:#D97706}
.st-replied{background:#D1FAE5;color:#059669}
.st-following{background:#DBEAFE;color:#2563EB}
.st-closed{background:#D1FAE5;color:#059669}
.st-lost{background:#F3F4F6;color:#9CA3AF}

.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px}
.card-title{font-size:13px;font-weight:600;color:var(--text-h);font-family:'Plus Jakarta Sans',sans-serif;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.cnt{font-size:11px;color:var(--text-f);font-weight:400}

.info-grid{display:flex;flex-direction:column;gap:0}
.info-row{display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #F3F4F6}
.info-row:last-child{border-bottom:none}
.info-label{font-size:11px;color:var(--text-f);width:68px;flex-shrink:0}
.info-val{font-size:13px;color:var(--text-h);font-weight:500;flex:1}
.info-val.id{font-family:'DM Sans',monospace;font-size:12px;color:var(--primary)}
.info-val.link{color:var(--primary);cursor:pointer}
.level-badge{font-size:11px;font-weight:600;padding:2px 8px;border-radius:6px}
.level-A{background:#FEE2E2;color:#DC2626}
.level-B{background:#DBEAFE;color:#2563EB}
.level-C{background:#F3F4F6;color:#6B7280}

.strategy-body{}
.str-priority{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;
  margin-bottom:10px;
}
.prio-high{background:#FEE2E2;color:#DC2626}
.prio-medium{background:#FEF3C7;color:#D97706}
.prio-low{background:#F3F4F6;color:#6B7280}
.prio-closed{background:#D1FAE5;color:#059669}
.str-content{display:flex;flex-direction:column;gap:6px}
.str-next,.str-expected{display:flex;flex-direction:column;gap:2px}
.str-label{font-size:10px;color:var(--text-f);text-transform:uppercase;letter-spacing:0.5px}
.str-val{font-size:12px;color:var(--text-m)}

.inquiries-card{}
.inq-list{display:flex;flex-direction:column;gap:8px}
.inq-entry{
  background:#F9FAFB;border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:12px;cursor:pointer;
  transition:border-color var(--transition),box-shadow var(--transition);
}
.inq-entry:hover{border-color:#BFDBFE;box-shadow:var(--shadow-sm)}
.ie-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.ie-product{font-size:13px;font-weight:600;color:var(--text-h)}
.ie-intent{font-size:10px;font-weight:600;padding:1px 6px;border-radius:10px}
.intent-high{background:#FEE2E2;color:#DC2626}
.intent-medium{background:#F0FDF4;color:#16A34A}
.intent-low{background:#F3F4F6;color:#6B7280}
.ie-meta{display:flex;align-items:center;gap:8px;margin-bottom:4px}
.ie-date{font-size:11px;color:var(--text-f)}
.ie-qty{font-size:11px;color:var(--text-f)}
.ie-status{font-size:11px;font-weight:600;padding:1px 6px;border-radius:10px;margin-left:auto}
.ie-summary{font-size:11px;color:var(--text-c);margin-bottom:4px;line-height:1.5}
.ie-action{font-size:11px;color:var(--primary);font-weight:600}
</style>

/* =============================================
   移动端适配 — 断点 768px
   ============================================= */
@media (max-width: 768px) {
  .mobile-header { display: flex !important; position: fixed; top: 0; left: 0; right: 0; z-index: 200; height: 56px; background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 16px; align-items: center; justify-content: space-between; box-shadow: var(--shadow-sm); }
  .mobile-logo { font-size: 15px; font-weight: 700; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--text-h); }
  .mobile-user { width: 32px; height: 32px; background: var(--primary); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 12px; }
  .hamburger { width: 36px; height: 36px; background: none; border: none; cursor: pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 5px; padding: 4px; border-radius: 6px; }
  .hamburger:hover { background: #F3F4F6; }
  .hamburger span { display: block; width: 20px; height: 2px; background: #374151; border-radius: 2px; }
  .sidebar-overlay { display: block; position: fixed; inset: 0; z-index: 299; background: rgba(0,0,0,0.4); opacity: 0; pointer-events: none; transition: opacity 0.2s; }
  .sidebar-overlay.show { opacity: 1; pointer-events: auto; }
  .sidebar { position: fixed; top: 0; left: 0; bottom: 0; z-index: 300; width: 240px; transform: translateX(-100%); box-shadow: var(--shadow-lg); transition: transform 0.2s; }
  .sidebar.sidebar-open { transform: translateX(0); }
  /* 移动端侧边栏：白色背景 */
  .sidebar {
    background: #FFFFFF !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.12) !important;
  }
  .sidebar .logo {
    color: #111827 !important;
    border-bottom-color: #E5E7EB !important;
  }
  .sidebar .logo span { color: #374151 !important; }
  .nav-item { color: #374151 !important; }
  .nav-item:hover { color: #2563EB !important; background: #EEF2FF !important; }
  .nav-item.active { color: #2563EB !important; background: #EEF2FF !important; }
  .nav-item.disabled { color: #9CA3AF !important; }

  .layout { padding-top: 56px; }
  .topbar { display: none !important; }
  .content { padding: 12px !important; }
  .ie-table-wrapper { overflow-x: auto; }
  .filters { flex-direction: column; }
}
