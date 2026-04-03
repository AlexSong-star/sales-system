<template>
  <div class="layout">

    <!-- 移动端顶栏 -->
    <header class="mobile-header">
      <button class="hamburger" @click="drawerOpen = !drawerOpen" aria-label="打开菜单">
        <span></span><span></span><span></span>
      </button>
      <div class="mobile-logo">📋 询盘管理</div>
      <div class="mobile-user">白</div>
    </header>

    <!-- 遮罩 -->
    <div class="sidebar-overlay" :class="{ show: drawerOpen }" @click="drawerOpen = false"></div>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-open': drawerOpen }">
      <div class="logo">📊 <span>销售系统</span></div>
      <nav class="nav">
        <div class="nav-item" @click="$router.push('/dashboard'); drawerOpen=false">
          <span class="icon">📊</span><span class="txt">仪表盘</span>
        </div>
        <div class="nav-item active">
          <span class="icon">📋</span><span class="txt">询盘管理</span>
        </div>
        <div class="nav-item" @click="$router.push('/customers'); drawerOpen=false">
          <span class="icon">👥</span><span class="txt">客户管理</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容 -->
    <div class="main">
      <header class="topbar">
        <div class="topbar-left">
          <div class="page-title">📋 询盘列表</div>
          <div class="page-sub">管理所有渠道的询盘</div>
        </div>
      </header>

      <div class="content">
        <div class="filters">
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
        <div class="list">
          <div
            v-for="item in filtered"
            :key="item.id"
            class="list-item"
            :class="{ 'is-danger': item.overHours > 24 }"
            @click="$router.push('/inquiry/' + item.id)"
          >
            <span class="item-ch">{{ chIcon(item.channel) }}</span>
            <div class="item-info">
              <div class="itemname">{{ item.customer }}</div>
              <div class="itempro">{{ item.product }}</div>
            </div>
            <div class="item-right">
              <div class="item-time">{{ item.time }}</div>
              <div class="item-st" :class="'st-' + item.status">{{ stLabel(item.status) }}</div>
            </div>
          </div>
          <div v-if="!filtered.length" class="empty">暂无数据</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const drawerOpen = ref(false)
const fChannel = ref('')
const fStatus = ref('')
const chIcon = (c) => ({ email:'📧', whatsapp:'💬', alibaba:'🛒' }[c] || '📌')
const stLabel = (s) => ({ pending:'待回复', replied:'已回复', following:'跟进中', closed:'已成交', invalid:'无效' }[s] || s)
const inquiries = ref([
  { id:1, channel:'email', customer:'Michael Johnson', product:'Paper Cups 50,000pcs', time:'2小时前', status:'following', overHours:5 },
  { id:2, channel:'whatsapp', customer:'Emma Schmidt', product:'Custom Boxes 5,000', time:'5小时前', status:'replied', overHours:0 },
  { id:3, channel:'alibaba', customer:'Li Wei', product:'Eco Bags 10,000', time:'1天前', status:'pending', overHours:26 },
  { id:4, channel:'email', customer:'Sarah Miller', product:'Paper Napkins 20,000pcs', time:'1天前', status:'closed', overHours:0 },
  { id:5, channel:'email', customer:'Ahmed Hassan', product:'Paper Cups 30,000', time:'2天前', status:'pending', overHours:26 },
])
const filtered = computed(() =>
  inquiries.value.filter(i => {
    if (fChannel.value && i.channel !== fChannel.value) return false
    if (fStatus.value && i.status !== fStatus.value) return false
    return true
  })
)
</script>

<style scoped>
:root {
  --bg: #F4F5F8; --surface: #FFFFFF; --border: #E5E7EB;
  --text-h: #111827; --text-m: #374151; --text-c: #6B7280; --text-f: #9CA3AF;
  --primary: #2563EB; --primary-hover: #1D4ED8;
  --sidebar-bg: #1E293B; --sidebar-text: rgba(255,255,255,0.55); --sidebar-text-active: #FFFFFF;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 2px 12px rgba(0,0,0,0.08); --shadow-lg: 0 8px 24px rgba(0,0,0,0.15);
  --radius: 12px; --radius-sm: 8px; --transition: 0.2s ease;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body,#app{height:100%;overflow:hidden}
body{font-family:'DM Sans','Noto Sans SC',system-ui,sans-serif;background:var(--bg);color:var(--text-h);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}

/* ========== 整体布局（桌面端） ========== */
.layout{display:flex;height:100vh;overflow:hidden;width:100vw}
.sidebar{width:180px;background:var(--sidebar-bg);display:flex;flex-direction:column;flex-shrink:0;z-index:10}
.logo{display:flex;align-items:center;gap:10px;padding:0 20px;height:64px;border-bottom:1px solid rgba(255,255,255,0.06);color:#fff;font-size:18px;font-family:'Plus Jakarta Sans',sans-serif;font-weight:700}
.logo span{font-size:13px;font-weight:700}
.nav{display:flex;flex-direction:column;padding:12px 0;gap:2px}
.nav-item{display:flex;align-items:center;padding:10px 20px;cursor:pointer;color:var(--sidebar-text);font-size:13px;gap:10px;transition:background var(--transition),color var(--transition)}
.nav-item:hover{color:var(--sidebar-text-active);background:rgba(255,255,255,0.06)}
.nav-item.active{color:var(--sidebar-text-active);background:rgba(37,99,235,0.55)}
.icon{font-size:16px;flex-shrink:0}
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}
.topbar{height:64px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;flex-shrink:0}
.topbar-left{display:flex;flex-direction:column;justify-content:center}
.page-title{font-size:18px;font-weight:700;color:var(--text-h);font-family:'Plus Jakarta Sans',sans-serif}
.page-sub{font-size:12px;color:var(--text-f);margin-top:1px}
.content{flex:1;overflow-y:auto;padding:14px 16px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.fsel{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm);padding:6px 10px;font-size:13px;color:var(--text-m);font-family:inherit;outline:none;cursor:pointer}
.list{display:flex;flex-direction:column;gap:8px}
.list-item{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);cursor:pointer;transition:box-shadow var(--transition)}
.list-item:hover{box-shadow:var(--shadow-md)}
.list-item.is-danger{border-left:3px solid #EF4444}
.item-ch{font-size:20px;flex-shrink:0}
.item-info{flex:1;min-width:0}
.itemname{font-size:14px;font-weight:600;color:var(--text-h);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.itempro{font-size:12px;color:var(--text-f);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.item-right{display:flex;flex-direction:column;align-items:flex-end;gap:3px;flex-shrink:0}
.item-time{font-size:11px;color:var(--text-f)}
.item-st{font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px}
.st-pending{background:#FEF3C7;color:#D97706}
.st-replied{background:#D1FAE5;color:#059669}
.st-following{background:#DBEAFE;color:#2563EB}
.st-closed{background:#D1FAE5;color:#059669}
.st-invalid{background:#F3F4F6;color:#9CA3AF}
.empty{text-align:center;color:var(--text-f);padding:40px;font-size:14px}

/* ========== 移动端顶栏（默认隐藏） ========== */
.mobile-header{
  display:none;position:fixed;top:0;left:0;right:0;z-index:200;
  height:56px;background:var(--surface);border-bottom:1px solid var(--border);
  padding:0 16px;align-items:center;justify-content:space-between;box-shadow:var(--shadow-sm);
}
.mobile-logo{font-size:15px;font-weight:700;font-family:'Plus Jakarta Sans',sans-serif;color:var(--text-h)}
.mobile-user{width:32px;height:32px;background:var(--primary);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:12px}
.hamburger{width:36px;height:36px;background:none;border:none;cursor:pointer;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:5px;padding:4px;border-radius:6px}
.hamburger:hover{background:#F3F4F6}
.hamburger span{display:block;width:20px;height:2px;background:#374151;border-radius:2px}
.sidebar-overlay{display:none;position:fixed;inset:0;z-index:299;background:rgba(0,0,0,0.4);opacity:0;transition:opacity var(--transition)}
.sidebar-overlay.show{display:block;opacity:1}

/* =============================================
   移动端适配 — 768px 及以下
   ============================================= */
@media (max-width: 768px) {
  /* 显示移动端顶栏 */
  .mobile-header { display: flex !important; }

  /* 侧边栏：抽屉式 + 白色背景 */
  .sidebar {
    position: fixed !important;
    top: 0; left: 0; bottom: 0;
    z-index: 300;
    width: 240px;
    transform: translateX(-100%);
    transition: transform var(--transition);
    background: #FFFFFF !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.12) !important;
  }
  .sidebar.sidebar-open { transform: translateX(0) !important; }
  .sidebar .logo { color: #111827 !important; border-bottom-color: #E5E7EB !important; }
  .sidebar .logo span { color: #374151 !important; }
  .sidebar .nav-item { color: #374151 !important; }
  .sidebar .nav-item:hover { color: #2563EB !important; background: #EEF2FF !important; }
  .sidebar .nav-item.active { color: #2563EB !important; background: #EEF2FF !important; }

  /* 主内容偏移 */
  .layout { padding-top: 56px; }

  /* 隐藏桌面端顶栏 */
  .topbar { display: none !important; }

  /* 内容区 */
  .content { padding: 12px; }
}
</style>
