import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import importPlugin from "eslint-plugin-import";
import jest from "eslint-plugin-jest";
import jsxA11y from "eslint-plugin-jsx-a11y";
import playwright from "eslint-plugin-playwright";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import testingLibrary from "eslint-plugin-testing-library";
import globals from "globals";

export default [
  {
    ignores: [
      "dist/**",
      "coverage/**",
      "node_modules/**",
      "playwright-report/**",
      "test-results/**",
      "quality-playground/**",
      "src/coupled/**",
    ],
  },

  js.configs.recommended,

  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "module",
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    plugins: {
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      import: importPlugin,
    },
    settings: { react: { version: "detect" } },
    rules: {
      ...react.configs.flat.recommended.rules,
      ...react.configs.flat["jsx-runtime"].rules,
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.flatConfigs.strict.rules,

      "no-console": "error",
      "no-var": "error",
      "prefer-const": "error",
      "prefer-template": "error",
      "object-shorthand": "error",
      eqeqeq: ["error", "always", { null: "ignore" }],
      "no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
      "no-param-reassign": "error",
      "no-nested-ternary": "warn",
      complexity: ["error", 12],
      "max-depth": ["error", 4],
      "max-lines-per-function": [
        "error",
        { max: 120, skipBlankLines: true, skipComments: true },
      ],

      "react/jsx-key": "error",
      "react/no-array-index-key": "off",
      "react/self-closing-comp": "error",
      "react/jsx-boolean-value": ["error", "never"],
      "react/prop-types": "off",

      "import/order": [
        "error",
        {
          groups: ["builtin", "external", "internal", "parent", "sibling", "index"],
          "newlines-between": "always",
          alphabetize: { order: "asc", caseInsensitive: true },
        },
      ],
      "import/no-duplicates": "error",
      "import/no-cycle": "error",
    },
  },

  {
    files: ["src/hooks/**/*.js"],
    rules: {
      "react-hooks/set-state-in-effect": "off",
    },
  },

  {
    files: ["test/**/*.{js,jsx}"],
    plugins: { jest, "testing-library": testingLibrary },
    languageOptions: { globals: { ...globals.jest } },
    rules: {
      ...jest.configs["flat/recommended"].rules,
      ...testingLibrary.configs["flat/react"].rules,
      "jest/expect-expect": "error",
      "jest/no-identical-title": "error",
      "jest/no-disabled-tests": "off",
      "jest/no-conditional-expect": "off",
      "max-lines-per-function": "off",
    },
  },

  {
    files: [
      "test/components/small-components.test.jsx",
      "test/components/ClassCard.test.jsx",
      "test/testability/**/*.jsx",
      "test/snapshots/**/*.jsx",
    ],
    rules: {
      "testing-library/no-container": "off",
      "testing-library/no-node-access": "off",
    },
  },

  {
    files: ["test/exercises/**/*.js"],
    rules: {
      "jest/expect-expect": "off",
      "jest/no-commented-out-tests": "off",
    },
  },

  {
    files: ["e2e/**/*.js"],
    plugins: { playwright },
    rules: {
      ...playwright.configs["flat/recommended"].rules,
      "max-lines-per-function": "off",
    },
  },

  prettier,
];
