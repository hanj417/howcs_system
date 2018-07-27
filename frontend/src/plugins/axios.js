import axios from 'axios'

const axiosConfig = {
  baseURL: 'https://howcs.kr:3000/api/v1'
}

export default ({ Vue }) => {
  Vue.prototype.$axios = axios.create(axiosConfig)
}
