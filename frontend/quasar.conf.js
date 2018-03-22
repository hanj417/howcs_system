// Configuration for your app

module.exports = function (ctx) {
  return {
    // app plugins (/src/plugins)
    plugins: [
      'i18n',
      'vuelidate',
      'axios',
      'bootstrap',
      'vueeditor',
      //'vue-html5-editor',
      //'jquery',
      //'lodash',
      //'common',
    ],
    css: [
      'app.styl',
      'bootstrap-3.3.5.custom.min.css',
      'styles.css',
    ],
    extras: [
      ctx.theme.mat ? 'roboto-font' : null,
      'material-icons'
      // 'ionicons',
      // 'mdi',
      // 'fontawesome'
    ],
    supportIE: false,
    vendor: {
      add: [],
      remove: []
    },
    build: {
      scopeHoisting: true,
      vueRouterMode: 'history',
      // gzip: true,
      // analyze: true,
      // extractCSS: false,
      // useNotifier: false,
      extendWebpack (cfg) {
/*
        cfg.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules|quasar)/
        })
*/
      }
    },
    devServer: {
      // https: true,
      host: '0.0.0.0',
      port: 6000,
      open: false // opens browser window automatically
    },
    // framework: 'all' --- includes everything; for dev only!
    framework: {
    i18n: 'ko-kr',
      components: [
    //'PostCard',
    'QCard',
    'QCardTitle',
    'QCardMain',
    'QCardMedia',
    'QCardSeparator',
    'QCardActions',
    'QUploader',
    'QVideo',
    'QModal',
    'QPageSticky',
    'QTabs',
    'QTab',
    'QTabPane',
    'QRouteTab',
        'QPopover',
        'QEditor',
        'QTable',
        'QTh',
        'QTr',
        'QTd',
        'QTableColumns',
        'QSearch',
        'QCollapsible',
        'QScrollObservable',
        'QOptionGroup',
        'QCard',
        'QCardTitle',
        'QCardMain',
        'QCardMedia',
        'QCardSeparator',
        'QCardActions',
        'QField',
        'QInput',
        'QDatetime',
        'QRadio',
        'QBreadcrumbs',
        'QBreadcrumbsEl',
        'QLayout',
        'QLayoutHeader',
        'QLayoutFooter',
        'QLayoutDrawer',
        'QPageContainer',
        'QPage',
        'QToolbar',
        'QToolbarTitle',
        'QBtn',
        'QBtnDropdown',
        'QIcon',
        'QList',
        'QListHeader',
        'QItem',
        'QItemMain',
        'QItemTile',
        'QItemSide'
      ],
      directives: [
        'Ripple'
      ],
      // Quasar plugins
      plugins: [
        'LocalStorage',
        'Notify'
      ]
    },
    // animations: 'all' --- includes all animations
    animations: [
    ],
    pwa: {
      cacheExt: 'js,html,css,ttf,eot,otf,woff,woff2,json,svg,gif,jpg,jpeg,png,wav,ogg,webm,flac,aac,mp4,mp3',
      manifest: {
        // name: 'Quasar App',
        // short_name: 'Quasar-PWA',
        // description: 'Best PWA App in town!',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#ffffff',
        theme_color: '#027be3',
        icons: [
          {
            'src': 'statics/icons/icon-128x128.png',
            'sizes': '128x128',
            'type': 'image/png'
          },
          {
            'src': 'statics/icons/icon-192x192.png',
            'sizes': '192x192',
            'type': 'image/png'
          },
          {
            'src': 'statics/icons/icon-256x256.png',
            'sizes': '256x256',
            'type': 'image/png'
          },
          {
            'src': 'statics/icons/icon-384x384.png',
            'sizes': '384x384',
            'type': 'image/png'
          },
          {
            'src': 'statics/icons/icon-512x512.png',
            'sizes': '512x512',
            'type': 'image/png'
          }
        ]
      }
    },
    cordova: {
      // id: 'org.cordova.quasar.app'
    },
    electron: {
      extendWebpack (cfg) {
        // do something with cfg
      },
      packager: {
        // OS X / Mac App Store
        // appBundleId: '',
        // appCategoryType: '',
        // osxSign: '',
        // protocol: 'myapp://path',

        // Window only
        // win32metadata: { ... }
      }
    },

    // leave this here for Quasar CLI
    starterKit: '1.0.0'
  }
}
