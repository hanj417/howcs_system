// import something here
// import { VueEditor } from 'vue2-quill-editor'
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

// leave the export, even if you don't use it
export default ({ Vue }) => {
  // something to do
//  Vue.use(VueEditor);
  Vue.use(VueQuillEditor /* { default global options } */)
}
