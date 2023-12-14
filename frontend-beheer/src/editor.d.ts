declare module 'quill' {
  import Quill from 'quill/core'

  export default Quill
}

declare module 'quill/modules/keyboard' {
  import Keyboard from 'quill/modules/keyboard'
  export default Keyboard
  export const keyBindings: any
}

declare module '@webspellchecker/wproofreader-sdk-js'
