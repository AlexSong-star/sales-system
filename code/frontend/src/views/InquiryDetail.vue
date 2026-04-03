<template>
  <div class="layout">

    <!-- 移动端顶栏 -->
    <header class="mobile-header" style="display:none">
      <button class="hamburger" @click="toggleDrawer" aria-label="打开菜单">
        <span></span><span></span><span></span>
      </button>
      <div class="mobile-logo">📋 询盘详情</div>
      <div class="mobile-user">白</div>
    </header>

    <!-- 侧边栏遮罩 -->
    <div class="sidebar-overlay" :class="{ show: drawerOpen }" @click="drawerOpen = false"></div>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-open': drawerOpen }">
      <div class="logo">📊 <span>销售系统</span></div>
      <nav class="nav">
        <div class="nav-item" @click="$router.push('/dashboard')">
          <span class="icon">📊</span><span class="txt">仪表盘</span>
        </div>
        <div class="nav-item active">
          <span class="icon">📋</span><span class="txt">询盘管理</span>
        </div>
        <div class="nav-item" @click="$router.push('/customers')">
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
          <button class="back-btn" @click="$router.push('/dashboard')">
            <span>←</span> 返回仪表盘
          </button>
        </div>
        <div class="topbar-right">
          <div class="user-avatar">白</div>
        </div>
      </header>

      <!-- 主体 -->
      <div class="content">

        <!-- 左侧：询盘信息 -->
        <div class="left">

          <!-- 基本信息卡 -->
          <div class="card info-card">
            <div class="card-header">
              <div class="card-title">
                <span class="ch-icon">{{ chIcon(inquiry.channel) }}</span>
                询盘详情
              </div>
              <div class="inq-st" :class="'st-' + inquiry.status">{{ stLabel(inquiry.status) }}</div>
            </div>

            <div class="info-grid">
              <div class="info-row">
                <span class="info-label">客户姓名</span>
                <span class="info-val">{{ inquiry.customer }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">客户邮箱</span>
                <span class="info-val link">{{ inquiry.email || '—' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">询盘产品</span>
                <span class="info-val">{{ inquiry.product }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">来源渠道</span>
                <span class="info-val">
                  <span class="ch-tag" :class="'ch-' + inquiry.channel">{{ chLabel(inquiry.channel) }}</span>
                </span>
              </div>
              <div class="info-row">
                <span class="info-label">收到时间</span>
                <span class="info-val">{{ inquiry.time }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">负责人</span>
                <span class="info-val owner">吕秀才</span>
              </div>
            </div>

            <!-- 快捷操作 -->
            <div class="quick-actions">
              <button class="btn btn-primary" @click="showReplyBox = !showReplyBox">
                📤 添加回复
              </button>
              <button class="btn" @click="showStatusBox = !showStatusBox">
                🏷 更新状态
              </button>
              <button class="btn btn-danger" @click="markInvalid" v-if="inquiry.status !== 'invalid'">
                ⚫ 标记无效
              </button>
            </div>

            <!-- 状态更新面板 -->
            <div class="panel" v-if="showStatusBox">
              <div class="panel-title">更新状态</div>
              <div class="status-options">
                <div
                  v-for="opt in statusOptions"
                  :key="opt.value"
                  class="status-opt"
                  :class="{ active: newStatus === opt.value }"
                  @click="newStatus = opt.value"
                >
                  <span class="opt-dot" :class="'dot-' + opt.value"></span>
                  {{ opt.label }}
                </div>
              </div>
              <button class="btn btn-primary btn-sm" @click="doUpdateStatus" :disabled="!newStatus">确认更新</button>
            </div>

          </div>

          <!-- 原始询盘 -->
          <div class="card msg-card">
            <div class="msg-header">
              <span class="msg-from">📩 客户询盘</span>
              <span class="msg-time">{{ inquiry.time }}</span>
            </div>
            <div class="msg-body customer">{{ inquiry.content }}</div>
          </div>

          <!-- 沟通记录 -->
          <div class="card msg-card" v-if="inquiry.replies && inquiry.replies.length">
            <div class="msg-header">
              <span class="msg-from">📤 吕秀才回复</span>
              <span class="reply-count">{{ inquiry.replies.length }} 条</span>
            </div>
            <div class="reply-list">
              <div class="reply-item" v-for="(r, i) in inquiry.replies" :key="i">
                <div class="reply-meta">
                  <span class="reply-num">回复 {{ i + 1 }}</span>
                  <span class="reply-time">{{ r.time }}</span>
                </div>
                <div class="reply-body">{{ r.content }}</div>
              </div>
            </div>
          </div>

        </div>

        <!-- 右侧：操作面板 -->
        <div class="right">

          <!-- 回复框 -->
          <div class="card reply-card" v-if="showReplyBox">
            <div class="card-title">📤 添加新回复</div>
            <div class="reply-form">
              <div class="form-hint">回复内容将自动保存到该询盘的沟通记录中</div>
              <textarea
                class="reply-textarea"
                v-model="replyContent"
                placeholder="在此输入回复内容..."
                rows="6"
              ></textarea>
              <div class="form-actions">
                <button class="btn" @click="cancelReply">取消</button>
                <button class="btn btn-primary" @click="submitReply" :disabled="!replyContent.trim()">发送回复</button>
              </div>
            </div>
          </div>

          <!-- 询盘动态 -->
          <div class="card timeline-card">
            <div class="card-title">📋 询盘动态</div>
            <div class="timeline">
              <div class="tl-item" v-for="(ev, i) in timeline" :key="i">
                <div class="tl-dot" :class="'tl-' + ev.type"></div>
                <div class="tl-info">
                  <div class="tl-text">{{ ev.text }}</div>
                  <div class="tl-time">{{ ev.time }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作日志 -->
          <div class="card log-card">
            <div class="card-title">🕐 操作记录</div>
            <div class="log-list">
              <div class="log-item" v-for="(lg, i) in logs" :key="i">
                <span class="log-time">{{ lg.time }}</span>
                <span class="log-text">{{ lg.text }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const drawerOpen = ref(false)
const showReplyBox = ref(false)
const showStatusBox = ref(false)
const toggleDrawer = () => { drawerOpen.value = !drawerOpen.value }
const replyContent = ref('')
const newStatus = ref('')

const statusOptions = [
  { value:'pending', label:'⏳ 待回复' },
  { value:'replied', label:'✅ 已回复' },
  { value:'following', label:'🔄 跟进中' },
  { value:'closed', label:'🏁 已成交' },
  { value:'invalid', label:'⚫ 无效' },
]

// Mock 数据（后续替换为 API 调用）
const inquiry = ref({
  id: 1,
  channel: 'email',
  customer: 'Michael Johnson',
  email: 'michael.j@coffeeshop.com',
  product: 'Paper Cups 50,000pcs',
  content: 'Hi, we are interested in your paper cups for our coffee shop chain. Could you send us the price for 50,000 pcs with custom logo? Please include sample options and delivery time to LA port. We need this urgently as we are planning to launch our new branches next month.',
  time: '2026-03-30 09:15',
  status: 'following',
  replies: [
    { time:'2026-03-30 14:30', content:'Dear Michael, Thank you for your inquiry. FOB price: USD 0.12/pc for 50,000 pcs. Sample: 5-7 days, fee refundable upon order. We accept T/T and L/C at sight.' },
    { time:'2026-03-30 16:45', content:'Dear Michael, Following up on our previous email. Just wanted to confirm if you have reviewed the quotation. We also have FSC certified materials available if you need environmental certification for your brand.' },
    { time:'2026-04-01 10:00', content:'Dear Michael, Any updates on your side? We can offer a 3% discount for orders placed before April 15. Looking forward to your response.' },
  ]
})

const timeline = [
  { type:'inquiry', text:'收到客户询盘', time:'2026-03-30 09:15' },
  { type:'reply', text:'吕秀才发送首封回复', time:'2026-03-30 14:30' },
  { type:'reply', text:'吕秀才跟进回复', time:'2026-03-30 16:45' },
  { type:'status', text:'状态更新为「跟进中」', time:'2026-03-30 16:50' },
]

const logs = [
  { time:'2026-03-30 14:30', text:'吕秀才 创建了这条询盘' },
  { time:'2026-03-30 14:30', text:'吕秀才 添加了回复' },
  { time:'2026-03-30 16:45', text:'吕秀才 添加了跟进回复' },
  { time:'2026-03-30 16:50', text:'系统 将状态更新为「跟进中」' },
]

const chIcon = (c) => ({ email:'📧', whatsapp:'💬', alibaba:'🛒' }[c] || '📌')
const chLabel = (c) => ({ email:'邮件', whatsapp:'WhatsApp', alibaba:'阿里站' }[c] || c)
const stLabel = (s) => ({ pending:'待回复', replied:'已回复', following:'跟进中', closed:'已成交', invalid:'无效' }[s] || s)

const submitReply = () => {
  if (!replyContent.value.trim()) return
  // TODO: 调用后端 API
  inquiry.value.replies.push({
    time: new Date().toLocaleString('zh-CN'),
    content: replyContent.value.trim()
  })
  replyContent.value = ''
  showReplyBox.value = false
}

const cancelReply = () => {
  replyContent.value = ''
  showReplyBox.value = false
}

const doUpdateStatus = () => {
  if (!newStatus.value) return
  inquiry.value.status = newStatus.value
  showStatusBox.value = false
  newStatus.value = ''
}

const markInvalid = () => {
  inquiry.value.status = 'invalid'
}
</script>

<style scoped>
/* CSS 变量 */
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
  -webkit-font-smoothing:antialiased;
}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px;border-radius:4px}
:focus:not(:focus-visible){outline:none}

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
.topbar-left{display:flex;align-items:center}
.topbar-right{display:flex;align-items:center;gap:16px}
.back-btn{
  display:flex;align-items:center;gap:6px;
  background:none;border:none;cursor:pointer;
  font-size:14px;color:var(--text-c);font-family:inherit;
  padding:6px 10px;border-radius:var(--radius-sm);
  transition:background var(--transition),color var(--transition);
}
.back-btn:hover{background:#F5F6FA;color:var(--text-h)}
.user-avatar{
  width:36px;height:36px;background:var(--primary);color:#fff;
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-weight:600;font-size:13px;
  font-family:'Plus Jakarta Sans',sans-serif;
  cursor:pointer;transition:opacity var(--transition);
}
.user-avatar:hover{opacity:0.85}

/* 内容 */
.content{display:flex;flex:1;overflow:hidden;gap:16px;padding:16px}

/* 左侧 */
.left{flex:1;display:flex;flex-direction:column;gap:14px;overflow-y:auto;min-width:0}

/* 右侧 */
.right{width:320px;flex-shrink:0;display:flex;flex-direction:column;gap:14px;overflow-y:auto}

/* 卡片 */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px}
.card-title{
  font-size:14px;font-weight:600;color:var(--text-h);
  font-family:'Plus Jakarta Sans',sans-serif;
  display:flex;align-items:center;gap:6px;margin-bottom:14px
}

/* 信息卡 */
.info-card{padding:20px}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
.card-header .card-title{font-size:16px;margin:0;display:flex;align-items:center;gap:8px}
.ch-icon{font-size:20px}
.inq-st{font-size:11px;font-weight:600;padding:3px 10px;border-radius:10px}
.st-pending{background:#FEF3C7;color:#D97706}
.st-replied{background:#D1FAE5;color:#059669}
.st-following{background:#DBEAFE;color:#2563EB}
.st-closed{background:#D1FAE5;color:#059669}
.st-invalid{background:#F3F4F6;color:#9CA3AF}

.info-grid{display:flex;flex-direction:column;gap:0}
.info-row{
  display:flex;align-items:center;
  padding:10px 0;
  border-bottom:1px solid #F3F4F6;
}
.info-row:last-child{border-bottom:none}
.info-label{font-size:12px;color:var(--text-f);width:80px;flex-shrink:0}
.info-val{font-size:13px;color:var(--text-h);font-weight:500;flex:1}
.info-val.link{color:var(--primary);cursor:pointer}
.info-val.link:hover{text-decoration:underline}
.info-val.owner{
  background:#EEF2FF;color:#2563EB;
  font-size:12px;padding:2px 8px;border-radius:6px;font-weight:600;
}
.ch-tag{font-size:12px;padding:2px 8px;border-radius:6px;font-weight:600}
.ch-email{background:#EEF2FF;color:#2563EB}
.ch-whatsapp{background:#F0FDF4;color:#16A34A}
.ch-alibaba{background:#FFF7ED;color:#EA580C}

/* 快捷操作 */
.quick-actions{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap}

/* 状态面板 */
.panel{margin-top:14px;background:#F9FAFB;border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px}
.panel-title{font-size:12px;font-weight:600;color:var(--text-c);margin-bottom:10px}
.status-options{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.status-opt{
  display:flex;align-items:center;gap:8px;
  padding:6px 10px;border-radius:6px;cursor:pointer;
  font-size:13px;color:var(--text-m);
  transition:background var(--transition);
}
.status-opt:hover{background:#F3F4F6}
.status-opt.active{background:#EEF2FF}
.opt-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-pending{background:#F59E0B}
.dot-replied{background:#10B981}
.dot-following{background:#2563EB}
.dot-closed{background:#059669}
.dot-invalid{background:#9CA3AF}

/* 消息卡 */
.msg-card{}
.msg-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.msg-from{font-size:13px;font-weight:600;color:var(--text-h)}
.msg-time{font-size:11px;color:var(--text-f)}
.reply-count{font-size:11px;color:var(--text-f);background:#F3F4F6;padding:2px 8px;border-radius:10px}
.msg-body{
  font-size:13px;color:var(--text-m);line-height:1.8;
  background:#F9FAFB;padding:14px;border-radius:var(--radius-sm);
  border-left:3px solid #3B82F6;
}
.reply-list{display:flex;flex-direction:column;gap:12px}
.reply-item{}
.reply-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.reply-num{font-size:11px;font-weight:600;color:var(--text-c)}
.reply-time{font-size:11px;color:var(--text-f)}
.reply-body{
  font-size:13px;color:var(--text-m);line-height:1.8;
  background:#F0FDF4;padding:12px;border-radius:var(--radius-sm);
  border-left:3px solid #22C55E;
}

/* 回复框 */
.reply-card{margin-top:0}
.reply-form{}
.form-hint{font-size:11px;color:var(--text-f);margin-bottom:10px}
.reply-textarea{
  width:100%;border:1px solid var(--border);border-radius:var(--radius-sm);
  padding:10px;font-size:13px;font-family:inherit;color:var(--text-m);
  background:#FAFAFA;resize:vertical;outline:none;
  transition:border-color var(--transition);
  box-sizing:border-box;
}
.reply-textarea:focus{border-color:var(--primary);background:#fff}
.form-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:10px}

/* 时间线 */
.timeline{display:flex;flex-direction:column;gap:0}
.tl-item{display:flex;gap:10px;position:relative;padding-bottom:14px}
.tl-item:last-child{padding-bottom:0}
.tl-item::before{
  content:'';position:absolute;
  left:5px;top:14px;bottom:0;
  width:1px;background:#E5E7EB;
}
.tl-item:last-child::before{display:none}
.tl-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:3px}
.tl-inquiry{background:#3B82F6}
.tl-reply{background:#22C55E}
.tl-status{background:#F59E0B}
.tl-log{background:#9CA3AF}
.tl-info{flex:1}
.tl-text{font-size:13px;color:var(--text-m);line-height:1.5}
.tl-time{font-size:11px;color:var(--text-f);margin-top:2px}

/* 操作日志 */
.log-list{display:flex;flex-direction:column;gap:8px}
.log-item{display:flex;flex-direction:column;gap:2px}
.log-time{font-size:11px;color:var(--text-f);font-family:'DM Sans',sans-serif}
.log-text{font-size:12px;color:var(--text-c)}

/* 按钮 */
.btn{
  background:var(--surface);border:1px solid var(--border);
  border-radius:7px;padding:6px 14px;
  font-size:12px;font-family:inherit;color:var(--text-m);
  cursor:pointer;transition:background var(--transition),border-color var(--transition);
}
.btn:hover{background:#F5F6FA;border-color:#D1D5DB}
.btn:disabled{opacity:0.5;cursor:not-allowed}
.btn-primary{background:var(--primary);border-color:var(--primary);color:#fff}
.btn-primary:hover{background:var(--primary-hover)}
.btn-primary:disabled{background:var(--primary);opacity:0.5}
.btn-danger{color:#DC2626;border-color:#FECACA;background:#FEF2F2}
.btn-danger:hover{background:#FEE2E2}
.btn-sm{padding:4px 10px;font-size:11px}
</style>

/* =============================================
   移动端适配 — 断点 768px
   InquiryDetail 复用 Dashboard 的 mobile 机制
   ============================================= */
@media (max-width: 768px) {
  /* 移动端顶栏 */
  .layout { position: relative; padding-top: 56px; }
  .mobile-header {
    display: flex !important;
    position: fixed; top: 0; left: 0; right: 0; z-index: 200;
    height: 56px; background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 16px;
    align-items: center; justify-content: space-between;
    box-shadow: var(--shadow-sm);
  }
  .mobile-header .mobile-logo {
    font-size: 15px; font-weight: 700;
    font-family: 'Plus Jakarta Sans', sans-serif; color: var(--text-h);
  }
  .mobile-header .mobile-user {
    width: 32px; height: 32px; background: var(--primary); color: #fff;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 600; font-size: 12px;
  }
  .hamburger {
    width: 36px; height: 36px; background: none; border: none; cursor: pointer;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    gap: 5px; padding: 4px; border-radius: 6px;
  }
  .hamburger:hover { background: #F3F4F6; }
  .hamburger span { display: block; width: 20px; height: 2px; background: #374151; border-radius: 2px; }
  .sidebar-overlay {
    display: block; position: fixed; inset: 0; z-index: 299;
    background: rgba(0,0,0,0.4); opacity: 0; pointer-events: none; transition: opacity 0.2s;
  }
  .sidebar-overlay.show { opacity: 1; pointer-events: auto; }
  .sidebar {
    position: fixed; top: 0; left: 0; bottom: 0; z-index: 300;
    transform: translateX(-100%); width: 240px;
    box-shadow: var(--shadow-lg); transition: transform 0.2s;
  }
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

  /* 隐藏桌面端顶栏 */
  .topbar { display: none !important; }
  /* 内容区调整 */
  .content { padding: 12px !important; flex-direction: column !important; gap: 12px !important; }
  .detail-main, .detail-side { width: 100% !important; flex: none !important; }
  .detail-side { min-width: 0 !important; }
  /* 表单移动端 */
  .detail-form { padding: 12px !important; }
  .form-row { flex-direction: column !important; gap: 8px !important; }
  .form-group { min-width: 0 !important; }
  .form-actions { flex-wrap: wrap !important; justify-content: flex-start !important; }
}
