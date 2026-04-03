import axios from 'axios'

const api = axios.create({
  baseURL: 'https://sales-system-production-0a91.up.railway.app',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

// 仪表盘统计
export const getStats = () => api.get('/api/dashboard/stats').then(r => r.data)
export const getTrend = (days = 7) => api.get(`/api/dashboard/trend?days=${days}`).then(r => r.data)

// 询盘
export const getInquiries = (params = {}) => api.get('/api/inquiries', { params }).then(r => r.data)
export const getInquiry = (id) => api.get(`/api/inquiries/${id}`).then(r => r.data)
export const updateInquiry = (id, data) => api.patch(`/api/inquiries/${id}`, data).then(r => r.data)
export const addReply = (inquiryId, content) => api.post(`/api/inquiries/${inquiryId}/replies`, { content }).then(r => r.data)

// 客户
export const getCustomers = (params = {}) => api.get('/api/customers', { params }).then(r => r.data)
export const getCustomer = (id) => api.get(`/api/customers/${id}`).then(r => r.data)
export const updateCustomer = (id, data) => api.patch(`/api/customers/${id}`, data).then(r => r.data)

export default api
