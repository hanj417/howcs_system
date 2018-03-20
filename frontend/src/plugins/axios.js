import axios from 'axios'

const axios_config = {
    baseURL: 'http://howcs.kr:3000/api',
}

export default ({ Vue }) => {
  Vue.prototype.$axios = axios.create(axios_config)
}
