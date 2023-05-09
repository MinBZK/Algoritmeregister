module.exports = {
  root: true,
  env: {
    node: true,
  },
  ignorePatterns: ['**/public/*'],
  extends: ['plugin:vue/vue3-recommended', '@vue/eslint-config-typescript'],
  rules: {
    'vue/multi-word-component-names': 'off',
    quotes: ['warn', 'single'],
    'object-curly-spacing': ['warn', 'always'],
    semi: ['warn', 'never'],
    'comma-dangle': [
      'warn',
      {
        arrays: 'always-multiline',
        objects: 'always-multiline',
        imports: 'always-multiline',
        exports: 'always-multiline',
      },
    ],
    'vue/max-attributes-per-line': [
      'warn',
      {
        singleline: 2,
        multiline: {
          max: 1,
        },
      },
    ],
    'vue/valid-v-slot': [
      'error',
      {
        allowModifiers: true,
      },
    ],
  },
}
