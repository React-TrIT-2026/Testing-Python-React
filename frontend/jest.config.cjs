module.exports = {
  testEnvironment: "jsdom",
  testEnvironmentOptions: {
    customExportConditions: [""],
  },
  setupFiles: ["<rootDir>/test/polyfills.js"],
  setupFilesAfterEnv: ["<rootDir>/test/setup.js"],
  clearMocks: true,
  restoreMocks: true,
  moduleNameMapper: {
    "\\.css$": "<rootDir>/test/styleMock.cjs",
  },
  collectCoverageFrom: ["src/**/*.{js,jsx}", "!src/main.jsx", "!src/coupled/**"],
  testMatch: ["<rootDir>/test/**/*.test.{js,jsx}"],
};
