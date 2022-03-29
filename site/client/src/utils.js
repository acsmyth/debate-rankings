require("dotenv").config();

const environment = process.env.NODE_ENV;
export const IS_DEV = environment === "development";
export const API_BASE_URL = IS_DEV
  ? "http://localhost:3000"
  : "https://www.debate-rankings.com/api";
