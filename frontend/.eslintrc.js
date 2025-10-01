module.exports = {
  extends: [
    'airbnb',
    'airbnb/hooks',
    'plugin:react/recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:import/react',
  ],
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  plugins: [
    'react',
    'import',
    'jsx-a11y',
    'react-hooks',
  ],
  rules: {
    'react/jsx-filename-extension': [1, { extensions: ['.js', '.jsx'] }],
    'react/jsx-one-expression-per-line': 'off',
    'react/jsx-no-undef': 1,
    'react/self-closing-comp': 1,
    'jsx-a11y/label-has-associated-control': [2, {
      assert: 'either',
    }],
    'no-use-before-define': [2, { functions: false, classes: true }],
    'comma-dangle': [2, 'always-multiline'],
    'react/prop-types': 'off',
    'react/button-has-type': 'off',
    'react/function-component-definition': 'off',
    'no-multiple-empty-lines': ['error', { max: 2, maxEOF: 0 }],
    'no-trailing-spaces': 'warn',
    'no-nested-ternary': 'off',
    'linebreak-style': 'off',
    'eol-last': ['error', 'always'],
  },
};
