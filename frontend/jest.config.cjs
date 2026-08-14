/** Configuración de Jest para los tests del frontend. */
module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  clearMocks: true,
  moduleNameMapper: {
    "\\.css$": "<rootDir>/test/styleMock.cjs",
  },
  collectCoverageFrom: ["src/**/*.{js,jsx}", "!src/main.jsx"],
};
