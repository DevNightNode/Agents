import { tool } from '@langchain/core/tools';
import { z } from 'zod';
import { Config } from './config.js';

const API_VERSION = '2024-07';
const BASE_URL = `https://${Config.SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/${API_VERSION}`;

// Minimal Shopify Admin REST client
async function shopify<T>(method: string, path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'X-Shopify-Access-Token': Config.SHOPIFY_ACCESS_TOKEN,
      'Content-Type': 'application/json',
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`Shopify ${method} ${path} failed: ${response.status} ${await response.text()}`);
  }
  return (await response.json()) as T;
}

interface Variant {
  id: number;
  title: string;
  sku: string;
  price: string;
  inventory_item_id: number;
  inventory_quantity: number;
  inventory_policy: string;
}

interface InventoryLevel {
  inventory_item_id: number;
  location_id: number;
  available: number | null;
}

export const get_inventory = tool(
  async ({ product_id }: { product_id: string }) => {
    try {
      const { product } = await shopify<{ product: { id: number; title: string; variants: Variant[] } }>(
        'GET',
        `/products/${product_id}.json`
      );

      const itemIds = product.variants.map((variant) => variant.inventory_item_id).join(',');
      const { inventory_levels } = await shopify<{ inventory_levels: InventoryLevel[] }>(
        'GET',
        `/inventory_levels.json?inventory_item_ids=${itemIds}`
      );

      return {
        product_id: product.id,
        title: product.title,
        variants: product.variants.map((variant) => ({
          id: variant.id,
          title: variant.title,
          sku: variant.sku,
          inventory_quantity: variant.inventory_quantity,
          inventory_policy: variant.inventory_policy,
        })),
        inventory_levels: inventory_levels.map((level) => ({
          inventory_item_id: level.inventory_item_id,
          available: level.available,
          location_id: level.location_id,
        })),
      };
    } catch (error) {
      return { error: `Failed to fetch inventory for product ${product_id}: ${error}` };
    }
  },
  {
    name: 'get_inventory',
    description: 'Fetches inventory levels for a specific product by product ID',
    schema: z.object({
      product_id: z.string().describe('The Shopify product ID to fetch inventory for'),
    }),
  }
);

export const update_price = tool(
  async ({ product_id, variant_id, new_price }: { product_id: string; variant_id: string; new_price: number }) => {
    try {
      const { variant } = await shopify<{ variant: Variant }>('PUT', `/variants/${variant_id}.json`, {
        variant: { id: Number(variant_id), price: new_price.toFixed(2) },
      });
      return {
        success: true,
        product_id,
        variant_id,
        new_price: variant.price,
        message: `Price updated successfully for variant ${variant_id}`,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to update price for variant ${variant_id}: ${error}`,
      };
    }
  },
  {
    name: 'update_price',
    description: 'Updates the price of a specific product variant',
    schema: z.object({
      product_id: z.string().describe('The Shopify product ID'),
      variant_id: z.string().describe('The variant ID to update'),
      new_price: z.number().describe('The new price value'),
    }),
  }
);

export const create_discount_code = tool(
  async ({ code, value, type, usage_limit }: { code: string; value: number; type: 'percentage' | 'fixed_amount'; usage_limit?: number }) => {
    try {
      // A discount code belongs to a price rule; create the rule first.
      const { price_rule } = await shopify<{ price_rule: { id: number } }>('POST', '/price_rules.json', {
        price_rule: {
          title: code,
          target_type: 'line_item',
          target_selection: 'all',
          allocation_method: 'across',
          value_type: type,
          value: `-${value}`,
          customer_selection: 'all',
          usage_limit: usage_limit ?? null,
          starts_at: new Date().toISOString(),
        },
      });
      const { discount_code } = await shopify<{ discount_code: { id: number } }>(
        'POST',
        `/price_rules/${price_rule.id}/discount_codes.json`,
        { discount_code: { code } }
      );
      return {
        success: true,
        price_rule_id: price_rule.id,
        discount_code_id: discount_code.id,
        code,
        value,
        type,
        usage_limit,
        message: `Discount code ${code} created successfully`,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to create discount code ${code}: ${error}`,
      };
    }
  },
  {
    name: 'create_discount_code',
    description: 'Creates a new discount code in Shopify',
    schema: z.object({
      code: z.string().describe('The discount code to create'),
      value: z.number().describe('The discount value'),
      type: z.enum(['percentage', 'fixed_amount']).describe('The type of discount'),
      usage_limit: z.number().optional().describe('Maximum number of times the discount can be used'),
    }),
  }
);
