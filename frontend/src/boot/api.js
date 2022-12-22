import axios from 'axios'

// let accessToken = ''
// let roleCd = 0
const api = axios.create({ baseURL: process.env.baseUrl })
// const apiAuth = axios.create({
//   baseURL: process.env.baseUrl,
//   headers: { Authorization: 'Bearer ' + accessToken }
// })

// function getRoleCd () {
//   return roleCd
// }

export { api }
