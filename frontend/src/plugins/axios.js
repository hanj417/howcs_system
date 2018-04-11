import axios from 'axios'

const axiosConfig = {
  baseURL: 'https://howcs.kr/api'
}

export default ({ Vue }) => {
  Vue.prototype.$axios = axios.create(axiosConfig)
}
