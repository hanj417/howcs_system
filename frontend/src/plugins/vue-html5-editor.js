// import something here
import VueHtml5Editor from 'vue-html5-editor'

// leave the export, even if you don't use it
export default ({ Vue }) => {
  // something to do
  Vue.use(VueHtml5Editor, {
    showModuleName: true,
    image: {
      sizeLimit: 512 * 1024,
      compress: true,
      width: 500,
      height: 500,
      quality: 80
    }
  })
}
