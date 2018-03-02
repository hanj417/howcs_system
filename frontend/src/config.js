const baseUrl = 'http://wonzi.net:3000'
const config = {
  url: baseUrl,
  ajaxUploadUrl: `${baseUrl}/admin/api/upload`,
  debug: {
    http: false // http request log
  },
  api: `${baseUrl}/api`
}

global.config = config

export default config
