import dotenv from 'dotenv';

dotenv.config();

export const Config = {
  SHOPIFY_SHOP_NAME: process.env['SHOPIFY_SHOP_NAME']!,
  SHOPIFY_ACCESS_TOKEN: process.env['SHOPIFY_ACCESS_TOKEN']!,
  OPENAI_API_KEY: process.env['OPENAI_API_KEY']!,
};
